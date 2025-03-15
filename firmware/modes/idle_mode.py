import setup_wifi
from setup_server import connect_server
from setup_buttons import setup_buttons
import time
import state

def idle_mode():
    """
    Modo reposo: mantiene la conexión Wi-Fi y con el servidor activa,
    y espera la activación por botones.
    """
    print("🟡 Entrando en modo reposo...")

    # Intentar conectar al Wi-Fi
    wlan = setup_wifi.connect_wifi()
    if not wlan or not wlan.isconnected():
        print("❌ No hay conexión Wi-Fi. Reintentando...")
        return  # Se reintentará desde boot.py

    # Intentar conectar al servidor
    sock = connect_server()
    if not sock:
        print("❌ No hay conexión con el servidor. Reintentando...")
        return  # Se reintentará desde boot.py

    state.recording = False  # 🔹 Cambiamos el estado global
    setup_buttons()

    while True:
        if not wlan.isconnected():
            print("❌ Conexión Wi-Fi perdida. Intentando reconectar...")
            wlan = setup_wifi.connect_wifi()
            if not wlan.isconnected():
                print("🔄 No se pudo reconectar. Retornando a boot...")
                return

        if sock:  # Comprobar si el socket sigue activo
            try:
                sock.send(b'PING')  # Intento de comunicación básica
            except Exception:
                print("❌ Conexión con el servidor perdida. Intentando reconectar...")
                sock = setup_server.connect_to_server()
                if not sock:
                    print("🔄 No se pudo reconectar con el servidor. Retornando a boot...")
                    return

        time.sleep(1)  # Evita sobrecargar el ESP32 con verificaciones constantes

