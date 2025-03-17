import network
import time
import machine
from setup import config 

wifi_config = config.load_config()
SSID = wifi_config.get("SSID", "default_SSID")
PASSWORD = wifi_config.get("PASSWORD", "default_PASSWORD")
wlan = network.WLAN(network.STA_IF) # Variable global 

led = machine.Pin(2, machine.Pin.OUT)  # LED indicador

def blink_led(times=3, delay=0.3):
    """Parpadea el LED para indicar estado"""
    for _ in range(times):
        led.on()
        time.sleep(delay)
        led.off()
        time.sleep(delay)

def connect_wifi(attempt=1, max_attempts=5):
    """Conectar a Wi-Fi con reintentos automáticos"""
    global wlan  # Usar la instancia global
    wlan.active(True)
    
    if wlan.isconnected():
        print(f"✅ Ya conectado a Wi-Fi: {wlan.ifconfig()[0]}")
        return wlan  # ✅ Retorna siempre la misma instancia

    print(f"🔄 Intentando conectar a Wi-Fi (SSID: {SSID})... Intento {attempt}/{max_attempts}")
    wlan.connect(SSID, PASSWORD)

    for _ in range(20):  
        if wlan.isconnected():
            print("✅ Conectado a Wi-Fi!")
            print("📡 Dirección IP:", wlan.ifconfig()[0])
            return wlan
        time.sleep(1)

    print(f"❌ Intento {attempt}/{max_attempts} fallido.")
    
    if attempt < max_attempts:
        return connect_wifi(attempt + 1, max_attempts)  # 🔄 Reintento
    else:
        print("🔄 Reiniciando ESP32 tras múltiples fallos...")
        time.sleep(2)
        machine.reset()

def get_wlan():
    """Obtener la instancia global de wlan sin redefinirla"""
    global wlan
    return wlan

