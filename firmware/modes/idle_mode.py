import time
from setup.buttons import setup_buttons
from setup.wifi import connect_wifi, get_wlan
from setup.server import connect_server
from modes import state

def start_idle_mode():
    """
    Modo reposo: mantiene la conexión Wi-Fi y con el servidor activa,
    y espera la activación por botones.
    """
    print("🟡 Entrando en modo reposo...")

    # 🔄 Intentar conectar a Wi-Fi
    wlan = connect_wifi()
    if not wlan or not wlan.isconnected():
        print("❌ No hay conexión Wi-Fi. Intentando conectar...")
        wlan = connect_wifi()
        if not wlan or not wlan.isconnected():
            print("🔄 No se pudo conectar a Wi-Fi. Retornando a boot...")
            return

    # 🔄 Intentar conectar al servidor
    #deprecado utilizar requests
    #sock = connect_server()
    
    #if not sock:
        #print("❌ No hay conexión con el servidor. Intentando de nuevo más tarde...")
        #return

    # ✅ Estado inicial
    state.recording = False  
    setup_buttons()

    while True:
        # 📡 Verificar Wi-Fi
        if not wlan.isconnected():
            print("❌ Wi-Fi perdido. Intentando reconectar...")
            wlan = connect_wifi()
            if not wlan or not wlan.isconnected():
                print("🔄 No se pudo reconectar. Retornando a boot...")
                return

        # 🔌 Verificar conexión con el servidor
      #deprecado, porfavor usar libreria requests

        time.sleep(1)  # Evita sobrecargar el ESP32 con verificaciones constantes

