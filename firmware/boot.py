import setup_sd
from setup_buttons import setup_buttons
import setup_wifi
import idle_mode  # Importamos el módulo de modo reposo
import machine
import time

# **Inicialización de hardware**
wlan = setup_wifi.connect_wifi()
led = machine.Pin(2, machine.Pin.OUT)

setup_buttons()  # Configurar los botones, pero solo se usarán en idle_mode

if wlan and wlan.isconnected():  
    print("✅ Wi-Fi conectado. Iniciando modo reposo...")
    idle_mode.start()  # Entra en modo reposo y espera interrupciones
else:
    print("❌ No hay conexión Wi-Fi. LED apagado.")

    # **Parpadeo de LED si no hay conexión Wi-Fi**
    for _ in range(10):  
        setup_wifi.blink_led(2, 0.5)  # Indica fallo en Wi-Fi
        time.sleep(0.5)
