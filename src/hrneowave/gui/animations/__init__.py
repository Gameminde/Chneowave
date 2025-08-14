# -*- coding: utf-8 -*-
"""
Module d'animations maritimes pour CHNeoWave
Phase 6 : Système d'animations et micro-interactions modernes
"""

# Imports principaux
from .animation_system import (
    MaritimeAnimator,
    AnimationType,
    AnimationPreset,
    get_animator,
    animate_widget
)

from .micro_interactions import (
    MaritimeMicroInteractions,
    InteractionState,
    get_micro_interactions
)

from .page_transitions import (
    MaritimePageTransitions,
    TransitionType,
    TransitionDirection
)

from .maritime_graphs import (
    MaritimeGraphStyle, 
    AnimatedPlotWidget, 
    MaritimeGraphManager,
    create_maritime_plot,
    apply_maritime_theme,
    get_maritime_graph_manager
)

# Version du module
__version__ = "1.0.0"

# Exports publics
__all__ = [
    # Animation System
    'MaritimeAnimator',
    'AnimationType',
    'AnimationPreset',
    'get_animator',
    'animate_widget',
    
    # Micro Interactions
    'MaritimeMicroInteractions',
    'InteractionState',
    'get_micro_interactions',
    
    # Page Transitions
    'MaritimePageTransitions',
    'TransitionType',
    'TransitionDirection',
    
    # Maritime Graphs
    'MaritimeGraphStyle',
    'AnimatedPlotWidget',
    'MaritimeGraphManager',
    'create_maritime_plot',
    'apply_maritime_theme',
    'get_maritime_graph_manager',
    
    # Fonctions utilitaires
    'setup_maritime_animations',
    'cleanup_animations'
]

# Instances globales
_global_animator = None
_global_micro_interactions = None
_global_page_transitions = None

def setup_maritime_animations(stacked_widget=None):
    """Configure le système d'animations maritimes global"""
    global _global_animator, _global_micro_interactions, _global_page_transitions
    
    # Initialiser l'animateur global
    if _global_animator is None:
        _global_animator = MaritimeAnimator()
    
    # Initialiser les micro-interactions globales
    if _global_micro_interactions is None:
        _global_micro_interactions = MaritimeMicroInteractions()
    
    # Initialiser les transitions de pages si un stacked_widget est fourni
    if stacked_widget is not None and _global_page_transitions is None:
        _global_page_transitions = MaritimePageTransitions(stacked_widget)
    
    return {
        'animator': _global_animator,
        'micro_interactions': _global_micro_interactions,
        'page_transitions': _global_page_transitions
    }

def cleanup_animations():
    """Nettoie toutes les animations en cours"""
    global _global_animator, _global_micro_interactions, _global_page_transitions
    
    if _global_animator:
        _global_animator.stop_all_animations()
    
    if _global_micro_interactions:
        _global_micro_interactions.cleanup_all_interactions()
    
    if _global_page_transitions:
        _global_page_transitions.stop_current_transition()

def get_animation_system():
    """Retourne le système d'animations complet"""
    return {
        'animator': get_animator(),
        'micro_interactions': get_micro_interactions(),
        'page_transitions': _global_page_transitions
    }