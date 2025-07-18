"""Alias pour circular_buffer.py - Compatibilité avec l'ancienne nomenclature

Ce module sert d'alias pour maintenir la compatibilité avec le code
qui importe spécifiquement 'lock_free_circular_buffer'.
"""

# Import de toutes les classes et fonctions du module principal
from .circular_buffer import (
    BufferConfig,
    BufferStats,
    CircularBufferBase,
    LockFreeCircularBuffer,
    MemoryMappedCircularBuffer,
    CircularBuffer,
    create_circular_buffer
)

# Alias principal pour compatibilité
CircularBuffer = LockFreeCircularBuffer

__all__ = [
    'BufferConfig',
    'BufferStats', 
    'CircularBufferBase',
    'LockFreeCircularBuffer',
    'MemoryMappedCircularBuffer',
    'CircularBuffer',
    'create_circular_buffer'
]