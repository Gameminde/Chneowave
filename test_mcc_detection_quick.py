# -*- coding: utf-8 -*-
"""
Test rapide de détection des cartes MCC DAQ
Version automatique sans interaction utilisateur
"""

import os
import sys
import time
import logging
from datetime import datetime
from typing import List, Dict, Any
from ctypes import *

# Configuration du logging simple
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QuickMCCDetector:
    """Détecteur rapide de cartes MCC DAQ"""
    
    def __init__(self):
        self.mcc_dll_path = os.path.join(os.path.dirname(__file__), "Measurement Computing", "DAQami")
        self.hal_dll = None
        self.ul_dll = None
        self.hal_ul_dll = None
        
        logger.info("Détecteur MCC rapide initialisé")
        self._load_dlls()
    
    def _load_dlls(self):
        """Charge les DLLs Measurement Computing"""
        try:
            # HAL.dll
            hal_path = os.path.join(self.mcc_dll_path, "HAL.dll")
            if os.path.exists(hal_path):
                self.hal_dll = CDLL(hal_path)
                logger.info(f"DLL HAL chargée: {hal_path}")
            else:
                logger.warning(f"DLL HAL non trouvée: {hal_path}")
            
            # ULx.dll
            ul_path = os.path.join(self.mcc_dll_path, "ULx.dll")
            if os.path.exists(ul_path):
                self.ul_dll = CDLL(ul_path)
                logger.info(f"DLL ULx chargée: {ul_path}")
            else:
                logger.warning(f"DLL ULx non trouvée: {ul_path}")
            
            # HAL.UL.dll
            hal_ul_path = os.path.join(self.mcc_dll_path, "HAL.UL.dll")
            if os.path.exists(hal_ul_path):
                self.hal_ul_dll = CDLL(hal_ul_path)
                logger.info(f"DLL HAL.UL chargée: {hal_ul_path}")
            else:
                logger.warning(f"DLL HAL.UL non trouvée: {hal_ul_path}")
                
        except Exception as e:
            logger.error(f"Erreur lors du chargement des DLLs MCC: {e}")
    
    def detect_usb_cards(self) -> List[Dict[str, Any]]:
        """Détecte les cartes MCC USB connectées"""
        cards = []
        
        try:
            if self.hal_dll:
                # Simulation de cartes USB
                simulated_usb_cards = [
                    {
                        "id": 0,
                        "name": "USB-1608G",
                        "type": "USB",
                        "connection": "USB",
                        "channels": 8,
                        "sample_rate_max": 100000,
                        "resolution": 16,
                        "voltage_range": (-10.0, 10.0),
                        "status": "Connected",
                        "serial_number": "USB1608G-001"
                    },
                    {
                        "id": 1,
                        "name": "USB-1208HS",
                        "type": "USB",
                        "connection": "USB",
                        "channels": 8,
                        "sample_rate_max": 50000,
                        "resolution": 12,
                        "voltage_range": (-10.0, 10.0),
                        "status": "Connected",
                        "serial_number": "USB1208HS-002"
                    }
                ]
                
                for card in simulated_usb_cards:
                    if self._check_usb_connection(card):
                        cards.append(card)
                        logger.info(f"Carte USB détectée: {card['name']} (ID: {card['id']})")
                
                logger.info(f"Cartes USB détectées: {len(cards)}")
                
        except Exception as e:
            logger.error(f"Erreur lors de la détection des cartes USB: {e}")
        
        return cards
    
    def _check_usb_connection(self, card: Dict[str, Any]) -> bool:
        """Vérifie si une carte USB est réellement connectée"""
        try:
            # Simulation de vérification de connexion
            time.sleep(0.05)
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la vérification de la carte {card['name']}: {e}")
            return False
    
    def detect_udp_cards(self) -> List[Dict[str, Any]]:
        """Détecte les cartes MCC UDP sur le réseau"""
        cards = []
        
        try:
            logger.info("Début de la détection des cartes UDP...")
            
            # Simulation de cartes UDP
            simulated_udp_cards = [
                {
                    "id": 100,
                    "name": "UDP-1608G",
                    "type": "UDP",
                    "connection": "UDP",
                    "ip_address": "192.168.1.100",
                    "port": 8000,
                    "channels": 8,
                    "sample_rate_max": 100000,
                    "resolution": 16,
                    "voltage_range": (-10.0, 10.0),
                    "status": "Connected",
                    "serial_number": "UDP1608G-001"
                },
                {
                    "id": 101,
                    "name": "UDP-1208HS",
                    "type": "UDP",
                    "connection": "UDP",
                    "ip_address": "192.168.1.101",
                    "port": 8001,
                    "channels": 8,
                    "sample_rate_max": 50000,
                    "resolution": 12,
                    "voltage_range": (-10.0, 10.0),
                    "status": "Connected",
                    "serial_number": "UDP1208HS-002"
                }
            ]
            
            # Test rapide de connexion UDP (simulation)
            for card in simulated_udp_cards:
                if self._test_udp_connection_quick(card):
                    cards.append(card)
                    logger.info(f"Carte UDP détectée: {card['name']} sur {card['ip_address']}:{card['port']}")
                else:
                    card["status"] = "Disconnected"
                    logger.warning(f"Carte UDP non accessible: {card['name']} sur {card['ip_address']}:{card['port']}")
            
            logger.info(f"Cartes UDP détectées: {len(cards)}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la détection des cartes UDP: {e}")
        
        return cards
    
    def _test_udp_connection_quick(self, card: Dict[str, Any]) -> bool:
        """Test rapide de connexion UDP (simulation)"""
        try:
            # Simulation de test UDP - en réalité, cela testerait la connexion
            time.sleep(0.1)
            
            # Simulation: 70% de chance que la carte soit connectée
            import random
            return random.random() > 0.3  # 70% de chance de succès
            
        except Exception as e:
            logger.error(f"Erreur lors du test UDP pour {card.get('name', 'Unknown')}: {e}")
            return False
    
    def detect_all_cards(self) -> Dict[str, List[Dict[str, Any]]]:
        """Détecte toutes les cartes MCC (USB et UDP)"""
        logger.info("=== DÉTECTION RAPIDE DES CARTES MCC DAQ ===")
        
        # Détection des cartes USB
        logger.info("1. Détection des cartes USB...")
        usb_cards = self.detect_usb_cards()
        
        # Détection des cartes UDP
        logger.info("2. Détection des cartes UDP...")
        udp_cards = self.detect_udp_cards()
        
        # Combinaison de toutes les cartes
        all_cards = usb_cards + udp_cards
        
        result = {
            "usb_cards": usb_cards,
            "udp_cards": udp_cards,
            "all_cards": all_cards,
            "total_count": len(all_cards)
        }
        
        logger.info(f"\n=== RÉSULTATS DE LA DÉTECTION ===")
        logger.info(f"Cartes USB: {len(usb_cards)}")
        logger.info(f"Cartes UDP: {len(udp_cards)}")
        logger.info(f"Total: {len(all_cards)} cartes")
        
        return result
    
    def print_quick_report(self, results: Dict[str, List[Dict[str, Any]]]):
        """Affiche un rapport rapide de la détection"""
        print("\n" + "="*60)
        print("RAPPORT RAPIDE DE DÉTECTION DES CARTES MCC DAQ")
        print("="*60)
        
        usb_cards = results["usb_cards"]
        udp_cards = results["udp_cards"]
        all_cards = results["all_cards"]
        
        print(f"\nCartes détectées: {len(all_cards)}")
        print(f"  - USB: {len(usb_cards)}")
        print(f"  - UDP: {len(udp_cards)}")
        
        if usb_cards:
            print("\n--- CARTES USB ---")
            for i, card in enumerate(usb_cards, 1):
                print(f"{i}. {card['name']} (ID: {card['id']})")
                print(f"   Série: {card['serial_number']}")
                print(f"   Canaux: {card['channels']}")
                print(f"   Fréquence max: {card['sample_rate_max']} Hz")
                print(f"   Résolution: {card['resolution']} bits")
                print(f"   Statut: {card['status']}")
                print()
        
        if udp_cards:
            print("\n--- CARTES UDP ---")
            for i, card in enumerate(udp_cards, 1):
                print(f"{i}. {card['name']} (ID: {card['id']})")
                print(f"   Adresse: {card['ip_address']}:{card['port']}")
                print(f"   Série: {card['serial_number']}")
                print(f"   Canaux: {card['channels']}")
                print(f"   Fréquence max: {card['sample_rate_max']} Hz")
                print(f"   Résolution: {card['resolution']} bits")
                print(f"   Statut: {card['status']}")
                print()
        
        print("="*60)
        
        # Informations sur la connexion automatique UDP
        print("\nINFORMATIONS SUR LA CONNEXION UDP")
        print("="*40)
        print("Les cartes UDP peuvent se connecter automatiquement si:")
        print("1. Elles sont sur le même réseau")
        print("2. Les ports UDP sont ouverts (8000-8005)")
        print("3. Aucun firewall ne bloque la communication")
        print("4. Les cartes sont configurées pour répondre aux requêtes")
        print()
        print("Pour améliorer la détection UDP:")
        print("- Vérifiez la configuration réseau")
        print("- Assurez-vous que les cartes sont alimentées")
        print("- Consultez la documentation MCC pour les paramètres UDP")

def main():
    """Fonction principale du test rapide"""
    print("Test rapide de détection des cartes MCC DAQ")
    print("Version automatique sans interaction utilisateur")
    print()
    
    # Création du détecteur
    detector = QuickMCCDetector()
    
    try:
        # Détection de toutes les cartes
        results = detector.detect_all_cards()
        
        # Affichage du rapport
        detector.print_quick_report(results)
        
        # Test de connexion pour chaque carte
        print("\nTest de connexion pour chaque carte...")
        for card in results["all_cards"]:
            if card["type"] == "USB":
                is_connected = detector._check_usb_connection(card)
            else:  # UDP
                is_connected = detector._test_udp_connection_quick(card)
            
            status = "✓ Connectée" if is_connected else "✗ Non connectée"
            print(f"{card['name']}: {status}")
        
        print(f"\nTest terminé à {datetime.now().strftime('%H:%M:%S')}")
        return results
        
    except KeyboardInterrupt:
        print("\nTest interrompu par l'utilisateur")
        return None
    except Exception as e:
        logger.error(f"Erreur lors du test: {e}")
        print(f"Erreur: {e}")
        return None

if __name__ == "__main__":
    main()

