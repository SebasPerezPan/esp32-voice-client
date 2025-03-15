import os

def load_config():
    """Carga las credenciales desde /sd/config.txt"""
    config = {}
    try:
        with open("/sd/config.txt", "r") as f:
            for line in f:
                key, value = line.strip().split("=")
                config[key] = value
    except Exception as e:
        print(f"❌ Error cargando configuración: {e}")
    
    return config

