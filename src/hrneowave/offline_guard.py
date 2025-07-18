"""Gardien pour empêcher les accès réseau en mode offline"""

import os
import socket
from functools import wraps


def check_offline_mode():
    """Vérifie si le mode offline est activé"""
    return os.getenv("CHNW_MODE", "offline") == "offline"


def network_guard(func):
    """Décorateur pour bloquer les fonctions réseau en mode offline"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if check_offline_mode():
            raise RuntimeError(
                f"Network access disabled in offline mode: {func.__name__}"
            )
        return func(*args, **kwargs)

    return wrapper


# Monkey-patch socket.create_connection
original_create_connection = socket.create_connection


def guarded_create_connection(*args, **kwargs):
    if check_offline_mode():
        raise RuntimeError("Network disabled in offline mode")
    return original_create_connection(*args, **kwargs)


socket.create_connection = guarded_create_connection
