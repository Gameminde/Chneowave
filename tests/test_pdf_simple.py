#!/usr/bin/env python3
"""
Test simple de génération PDF
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from hrneowave.utils.calib_pdf import CalibrationPDFGenerator

def test_simple_pdf():
    """Test simple de génération PDF"""
    
    # Données de test minimales
    sample_data = {
        'sensor_count': 1,
        'sensors': [
            {
                'id': 1,
                'name': 'Capteur Test',
                'gain': 1.0,
                'offset': 0.0,
                'r_squared': 0.999
            }
        ]
    }
    
    output_file = 'test_simple.pdf'
    
    try:
        print("=== Test de génération PDF simple ===")
        generator = CalibrationPDFGenerator()
        
        # Test de génération
        success = generator.generate_certificate(sample_data, output_file)
        
        if success:
            print("✓ PDF généré avec succès")
            
            # Vérifier que le fichier existe
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"✓ Fichier créé: {output_file} ({file_size} bytes)")
                
                # Lire les premiers octets pour vérifier le format PDF
                with open(output_file, 'rb') as f:
                    header = f.read(10)
                    if header.startswith(b'%PDF'):
                        print("✓ Format PDF valide")
                    else:
                        print(f"❌ Format PDF invalide: {header}")
                
                # Nettoyage
                os.remove(output_file)
                print("✓ Fichier nettoyé")
            else:
                print("❌ Fichier PDF non créé")
        else:
            print("❌ Échec de la génération PDF")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_simple_pdf()