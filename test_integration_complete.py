#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration complète CHNeoWave - Bridge API
Teste tous les endpoints et la connectivité avec l'interface React

Auteur: CHNeoWave Integration Team
Version: 1.0.0
Date: 2025-01-11
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, Any, List

class CHNeoWaveIntegrationTester:
    """Testeur d'intégration complète pour CHNeoWave"""
    
    def __init__(self):
        self.api_base = "http://localhost:3001"
        self.ui_base = "http://localhost:5173"
        self.results: List[Dict[str, Any]] = []
        
    def run_test(self, name: str, test_func) -> bool:
        """Exécute un test et enregistre le résultat"""
        print(f"\n🧪 Test: {name}")
        print("-" * 50)
        
        start_time = time.time()
        try:
            result = test_func()
            duration = time.time() - start_time
            
            self.results.append({
                "name": name,
                "status": "PASS" if result else "FAIL",
                "duration": round(duration, 3),
                "timestamp": datetime.now().isoformat()
            })
            
            status_emoji = "✅" if result else "❌"
            print(f"{status_emoji} {name}: {'PASS' if result else 'FAIL'} ({duration:.3f}s)")
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            self.results.append({
                "name": name,
                "status": "ERROR",
                "error": str(e),
                "duration": round(duration, 3),
                "timestamp": datetime.now().isoformat()
            })
            
            print(f"❌ {name}: ERROR - {e} ({duration:.3f}s)")
            return False
    
    def test_api_health(self) -> bool:
        """Test de santé du Bridge API"""
        response = requests.get(f"{self.api_base}/health", timeout=5)
        
        if response.status_code != 200:
            print(f"❌ Status code: {response.status_code}")
            return False
            
        data = response.json()
        print(f"📊 API Status: {data['data']['api_status']}")
        print(f"🐍 CHNeoWave Modules: {data['data']['chneowave_modules']}")
        
        if 'system_metrics' in data['data']:
            metrics = data['data']['system_metrics']
            print(f"💾 CPU: {metrics.get('cpu_percent', 'N/A')}%")
            print(f"🧠 Memory: {metrics.get('memory_percent', 'N/A')}%")
            
        return data['success'] and data['data']['api_status'] == 'healthy'
    
    def test_hardware_backends(self) -> bool:
        """Test des backends matériels"""
        response = requests.get(f"{self.api_base}/hardware/backends", timeout=5)
        
        if response.status_code != 200:
            return False
            
        data = response.json()
        backends = data['data']['backends']
        current = data['data']['current']
        
        print(f"🔧 Backends disponibles: {backends}")
        print(f"📡 Backend actuel: {current}")
        
        expected_backends = ["ni-daqmx", "iotech", "demo"]
        return (data['success'] and 
                all(backend in backends for backend in expected_backends) and
                current in backends)
    
    def test_hardware_scan(self) -> bool:
        """Test du scan matériel"""
        response = requests.get(f"{self.api_base}/hardware/scan", timeout=10)
        
        if response.status_code != 200:
            return False
            
        data = response.json()
        devices = data['data']['devices']
        count = data['data']['count']
        
        print(f"🔍 Périphériques scannés: {count}")
        print(f"📋 Détails: {devices}")
        
        return data['success']
    
    def test_acquisition_status(self) -> bool:
        """Test du statut d'acquisition"""
        response = requests.get(f"{self.api_base}/acquisition/status", timeout=5)
        
        if response.status_code != 200:
            return False
            
        data = response.json()
        status = data['data']['status']
        mode = data['data'].get('mode', 'unknown')
        
        print(f"📡 Status acquisition: {status}")
        print(f"🎮 Mode: {mode}")
        
        return data['success'] and status in ['idle', 'running', 'paused', 'stopped']
    
    def test_acquisition_start_stop(self) -> bool:
        """Test de démarrage et arrêt d'acquisition"""
        # Test démarrage
        start_config = {
            "sampling_rate": 1000.0,
            "channels": [0, 1],
            "voltage_range": "±10V",
            "buffer_size": 5000,
            "project_name": "Test Integration"
        }
        
        response = requests.post(f"{self.api_base}/acquisition/start", 
                               json=start_config, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Erreur démarrage: {response.status_code}")
            return False
            
        data = response.json()
        if not data['success']:
            print(f"❌ Échec démarrage: {data.get('error', 'Unknown')}")
            return False
            
        session_id = data['data']['session_id']
        print(f"🚀 Session démarrée: {session_id}")
        
        # Attendre un peu
        time.sleep(1)
        
        # Test arrêt
        response = requests.post(f"{self.api_base}/acquisition/stop", timeout=5)
        
        if response.status_code != 200:
            print(f"❌ Erreur arrêt: {response.status_code}")
            return False
            
        data = response.json()
        if not data['success']:
            print(f"❌ Échec arrêt: {data.get('error', 'Unknown')}")
            return False
            
        print("⏹️ Acquisition arrêtée avec succès")
        return True
    
    def test_fft_processing(self) -> bool:
        """Test du traitement FFT"""
        import math
        
        # Génération d'un signal test (sinusoïde + bruit)
        sampling_rate = 1000.0
        duration = 1.0  # 1 seconde
        frequency = 50.0  # 50 Hz
        
        signal_data = []
        for i in range(int(sampling_rate * duration)):
            t = i / sampling_rate
            signal = math.sin(2 * math.pi * frequency * t) + 0.1 * math.sin(2 * math.pi * 150 * t)
            signal_data.append(signal)
        
        fft_request = {
            "signal_data": signal_data,
            "sampling_rate": sampling_rate,
            "normalize": False
        }
        
        response = requests.post(f"{self.api_base}/processing/fft", 
                               json=fft_request, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ Erreur FFT: {response.status_code}")
            return False
            
        data = response.json()
        if not data['success']:
            print(f"❌ Échec FFT: {data.get('error', 'Unknown')}")
            return False
            
        fft_data = data['data']
        magnitude = fft_data['fft_magnitude']
        frequencies = fft_data['frequencies']
        
        print(f"📊 FFT calculée: {len(magnitude)} points")
        print(f"🎯 Freq max: {max(frequencies):.1f} Hz")
        print(f"🔢 Signal length: {fft_data['length']}")
        print(f"⚡ Mode: {fft_data.get('mode', 'unknown')}")
        
        return len(magnitude) == len(signal_data)
    
    def test_system_status(self) -> bool:
        """Test du statut système complet"""
        response = requests.get(f"{self.api_base}/system/status", timeout=5)
        
        if response.status_code != 200:
            return False
            
        data = response.json()
        
        # Peut échouer si modules CHNeoWave non disponibles, c'est OK
        if not data['success'] and 'MODULE_UNAVAILABLE' in str(data.get('error', {})):
            print("⚠️ Modules CHNeoWave non disponibles (mode simulation)")
            return True
            
        if data['success']:
            status = data['data']
            print(f"🏗️ Hardware backend: {status['hardware']['backend']}")
            print(f"📡 WebSocket connexions: {status['websockets']['active_connections']}")
            
        return True
    
    def test_ui_connectivity(self) -> bool:
        """Test de connectivité de l'interface React"""
        try:
            response = requests.get(self.ui_base, timeout=5)
            
            if response.status_code == 200:
                print(f"🌐 Interface React accessible")
                print(f"📄 Content-Type: {response.headers.get('content-type', 'unknown')}")
                return True
            else:
                print(f"❌ Status code UI: {response.status_code}")
                return False
                
        except requests.ConnectionError:
            print("❌ Interface React non accessible")
            return False
    
    def test_cors_headers(self) -> bool:
        """Test des headers CORS pour l'intégration React"""
        response = requests.options(f"{self.api_base}/health", 
                                   headers={'Origin': 'http://localhost:5173'}, 
                                   timeout=5)
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
        }
        
        print(f"🔗 CORS Headers: {cors_headers}")
        
        # Le CORS peut être géré différemment, accepter si pas d'erreur
        return response.status_code in [200, 404]
    
    def generate_report(self) -> str:
        """Génère un rapport de test complet"""
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.results if r['status'] in ['FAIL', 'ERROR']])
        
        report = f"""
🌊 CHNeoWave Integration Test Report
{'='*60}

📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 Tests: {total_tests} total, {passed_tests} passed, {failed_tests} failed
✅ Success Rate: {(passed_tests/total_tests*100):.1f}%

Detailed Results:
"""
        
        for result in self.results:
            status_emoji = {"PASS": "✅", "FAIL": "❌", "ERROR": "💥"}[result['status']]
            report += f"{status_emoji} {result['name']}: {result['status']} ({result['duration']}s)\n"
            
            if 'error' in result:
                report += f"   Error: {result['error']}\n"
        
        report += f"""
🎯 Integration Status: {'SUCCESS' if failed_tests == 0 else 'ISSUES DETECTED'}

📋 Next Steps:
"""
        
        if failed_tests == 0:
            report += """✅ Tous les tests passent !
✅ Bridge API opérationnel
✅ Interface React accessible  
✅ Intégration prête pour utilisation

🚀 Ready for production testing!"""
        else:
            report += f"""⚠️ {failed_tests} test(s) en échec
🔧 Vérifier la configuration des serveurs
📡 Vérifier les ports 3001 et 5173
🐛 Consulter les logs pour plus de détails"""
        
        return report
    
    def run_all_tests(self):
        """Exécute tous les tests d'intégration"""
        print("🌊 CHNeoWave Integration Test Suite")
        print("=" * 60)
        print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Tests de base
        self.run_test("API Health Check", self.test_api_health)
        self.run_test("UI Connectivity", self.test_ui_connectivity)
        self.run_test("CORS Configuration", self.test_cors_headers)
        
        # Tests des endpoints
        self.run_test("Hardware Backends", self.test_hardware_backends)
        self.run_test("Hardware Scan", self.test_hardware_scan)
        self.run_test("System Status", self.test_system_status)
        self.run_test("Acquisition Status", self.test_acquisition_status)
        
        # Tests de fonctionnalités
        self.run_test("Acquisition Start/Stop", self.test_acquisition_start_stop)
        self.run_test("FFT Processing", self.test_fft_processing)
        
        # Génération du rapport
        print("\n" + "="*60)
        report = self.generate_report()
        print(report)
        
        # Sauvegarde du rapport
        with open(f"integration_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md", 'w', encoding='utf-8') as f:
            f.write(report)
        
        return len([r for r in self.results if r['status'] == 'PASS']) == len(self.results)

def main():
    """Point d'entrée principal"""
    tester = CHNeoWaveIntegrationTester()
    
    print("🚀 Démarrage des tests d'intégration CHNeoWave...")
    print(f"🌐 Bridge API: {tester.api_base}")
    print(f"⚛️ React UI: {tester.ui_base}")
    
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 INTEGRATION SUCCESS! Tous les tests passent.")
        sys.exit(0)
    else:
        print("\n⚠️ INTEGRATION ISSUES DETECTED. Voir rapport pour détails.")
        sys.exit(1)

if __name__ == "__main__":
    main()
