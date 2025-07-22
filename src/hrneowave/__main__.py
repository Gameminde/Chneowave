#!/usr/bin/env python3
"""
Point d'entrée principal pour CHNeoWave
Utilisation: python -m hrneowave [commande] [options]
"""

if __name__ == "__main__":
    import argparse
    from .cli import run_cli
    run_cli()