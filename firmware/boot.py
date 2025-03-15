import machine
import time
from setup import setup_sd, setup_wifi, setup_buttons
from modules import idle_mode

# **Montar SD card**
try:
    setup_sd.mount_sd()
    print("✅ SD card montada correctamente.")
except Exception as e:
    print(f"⚠️ Error montando SD: {e}")

# **Configurar y conectar WiFi**
wlan = setup_wifi.connect_wifi()
if wlan and wlan.isconnected():
    print("✅ WiFi conectado.")
else:
    print("❌ No hay conexión WiFi. Intentando de nuevo...")
    
    for _ in range(5):
        setup_wifi.blink_led(2, 0.5)
        time.sleep(0.5)
    
    # Si después de 5 intentos sigue sin conectarse, reinicia el ESP32
    print("🔄 Reiniciando ESP32...")
    time.sleep(2)
    machine.reset()

# **Configurar botones**
setup_buttons()

# **Entrar en modo de espera**
print("⏳ Entrando en modo reposo...")
idle_mode.start()
