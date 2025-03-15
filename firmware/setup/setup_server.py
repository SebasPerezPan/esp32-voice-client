import socket
import time
import machine
import setup_config

config = setup_config.load_config()
SERVER_HOST = config.get("SERVER_HOST")
SERVER_PORT = int(config.get("SERVER_PORT"))

def connect_server():
    """Intentar conectarse al servidor"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)  
    try:
        print("🔗 Intentando conectar al servidor...")
        sock.connect((SERVER_HOST, SERVER_PORT))
        print("✅ Conectado al servidor!")
        return sock
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return None

led = machine.Pin(2, machine.Pin.OUT)  # LED indicador

def blink_led(times=3, delay=0.3):
    """Parpadea el LED para indicar estado"""
    for _ in range(times):
        led.on()
        time.sleep(delay)
        led.off()
        time.sleep(delay)

def connect_server():
    """Intenta conectarse al servidor"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)  # Tiempo de espera para conexión
    try:
        print("🔗 Intentando conectar al servidor...")
        sock.connect((SERVER_HOST, SERVER_PORT))
        print("✅ Conectado al servidor!")
        led.on()  # Encender LED cuando se conecta
        return sock
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return None

# Conectar al servidor automáticamente al importar
server_socket = connect_server()

