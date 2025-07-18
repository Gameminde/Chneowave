#!/usr/bin/env python3
"""
Interface en ligne de commande pour CHNeoWave
Commandes disponibles: gui, simulate, batch
"""

import argparse
import sys
from typing import Optional, List


def run_gui(args):
    """Lance l'interface graphique CHNeoWave complète"""
    try:
        import os
        from PyQt5.QtWidgets import QApplication
        from hrneowave.gui.main import HRNeoWaveApp
        
        # Configurer les variables d'environnement pour l'interface
        if args.simulate:
            os.environ['CHNW_MODE'] = 'simulate'
        if args.fs:
            os.environ['CHNW_FS'] = str(args.fs)
        if args.channels:
            os.environ['CHNW_CHANNELS'] = str(args.channels)
        if args.config:
            os.environ['CHNW_CONFIG'] = args.config
            
        # Créer l'application Qt si elle n'existe pas
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave")
            app.setApplicationVersion("3.0")
            app.setOrganizationName("Laboratoire Maritime")
            
        # Créer et lancer l'application complète
        main_app = HRNeoWaveApp(use_new_interface=True)
        main_app.show()
        
        print("🚀 CHNeoWave - Interface complète lancée")
        
        # Lancer la boucle d'événements
        sys.exit(app.exec_())
        
    except ImportError as e:
        print(f"❌ Erreur: Modules GUI non disponibles - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors du lancement de l'interface: {e}")
        sys.exit(1)


def run_simulate(args):
    """Lance CHNeoWave en mode simulation avec interface complète"""
    try:
        import os
        from PyQt5.QtWidgets import QApplication
        from hrneowave.gui.main import HRNeoWaveApp
        
        # Configurer les variables d'environnement pour la simulation
        os.environ['CHNW_MODE'] = 'simulate'
        if args.fs:
            os.environ['CHNW_FS'] = str(args.fs)
        if args.channels:
            os.environ['CHNW_CHANNELS'] = str(args.channels)
        if args.duration:
            os.environ['CHNW_DURATION'] = str(args.duration)
            
        # Créer l'application Qt si elle n'existe pas
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave")
            app.setApplicationVersion("3.0")
            app.setOrganizationName("Laboratoire Maritime")
            
        # Créer et lancer l'application complète en mode simulation
        main_app = HRNeoWaveApp(use_new_interface=True)
        main_app.show()
        
        print(f"🚀 CHNeoWave - Simulation lancée: fs={args.fs}Hz, channels={args.channels}, durée={args.duration}s")
        
        # Lancer la boucle d'événements
        sys.exit(app.exec_())
        
    except ImportError as e:
        print(f"❌ Erreur: Modules de simulation non disponibles - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors de la simulation: {e}")
        sys.exit(1)


def run_batch(args):
    """Lance CHNeoWave en mode batch (traitement par lots)"""
    try:
        from hrneowave.core.batch_processor import BatchProcessor
        
        if not args.input_dir:
            print("❌ Erreur: --input-dir requis pour le mode batch")
            sys.exit(1)
            
        processor = BatchProcessor(
            input_dir=args.input_dir,
            output_dir=args.output_dir or args.input_dir,
            config_file=args.config
        )
        
        print(f"📁 Traitement batch: {args.input_dir} → {args.output_dir or args.input_dir}")
        processor.process_all()
        print("✅ Traitement batch terminé")
        
    except ImportError as e:
        print(f"❌ Erreur: Modules de traitement batch non disponibles - {e}")
        print("💡 Astuce: Utilisez 'gui' ou 'simulate' pour l'interface graphique")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors du traitement batch: {e}")
        sys.exit(1)


def create_parser() -> argparse.ArgumentParser:
    """Crée le parser principal avec sous-commandes"""
    parser = argparse.ArgumentParser(
        prog='hrneowave',
        description='CHNeoWave - Logiciel d\'acquisition et d\'analyse maritime',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python -m hrneowave gui --simulate
  python -m hrneowave simulate --fs 64 --channels 16
  python -m hrneowave batch --input-dir ./data --output-dir ./results
"""
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        help='Commandes disponibles',
        metavar='COMMANDE'
    )
    
    # Commande GUI
    gui_parser = subparsers.add_parser(
        'gui',
        help='Lance l\'interface graphique'
    )
    gui_parser.add_argument(
        '--simulate',
        action='store_true',
        help='Active le mode simulation'
    )
    gui_parser.add_argument(
        '--fs',
        type=int,
        default=32,
        help='Fréquence d\'échantillonnage (Hz, défaut: 32)'
    )
    gui_parser.add_argument(
        '--channels',
        type=int,
        default=8,
        help='Nombre de canaux (défaut: 8)'
    )
    gui_parser.add_argument(
        '--config',
        type=str,
        help='Fichier de configuration'
    )
    
    # Commande SIMULATE
    sim_parser = subparsers.add_parser(
        'simulate',
        help='Lance une simulation'
    )
    sim_parser.add_argument(
        '--fs',
        type=int,
        default=32,
        help='Fréquence d\'échantillonnage (Hz, défaut: 32)'
    )
    sim_parser.add_argument(
        '--channels',
        type=int,
        default=8,
        help='Nombre de canaux (défaut: 8)'
    )
    sim_parser.add_argument(
        '--duration',
        type=int,
        default=60,
        help='Durée de simulation en secondes (défaut: 60)'
    )
    
    # Commande BATCH
    batch_parser = subparsers.add_parser(
        'batch',
        help='Traitement par lots'
    )
    batch_parser.add_argument(
        '--input-dir',
        type=str,
        required=True,
        help='Répertoire d\'entrée'
    )
    batch_parser.add_argument(
        '--output-dir',
        type=str,
        help='Répertoire de sortie (défaut: même que input-dir)'
    )
    batch_parser.add_argument(
        '--config',
        type=str,
        help='Fichier de configuration'
    )
    
    return parser


def run_cli(argv: Optional[List[str]] = None):
    """Point d'entrée principal de la CLI"""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Dispatch vers la fonction appropriée
    if args.command == 'gui':
        run_gui(args)
    elif args.command == 'simulate':
        run_simulate(args)
    elif args.command == 'batch':
        run_batch(args)
    else:
        print(f"❌ Commande inconnue: {args.command}")
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    run_cli()