import network
import time
import machine
import setup_config

config = setup_config.load_config()
SSID = config.get("SSID", "default_SSID")
PASSWORD = config.get("PASSWORD", "default_PASSWORD")

led = machine.Pin(2, machine.Pin.OUT)  # LED indicador

def blink_led(times=3, delay=0.3):
    """Parpadea el LED para indicar estado"""
    for _ in range(times):
        led.on()
        time.sleep(delay)
        led.off()
        time.sleep(delay)

def connect_wifi():
    """Conectar a Wi-Fi y parpadear mientras intenta"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("🔄 Conectando a Wi-Fi...")
        wlan.connect(SSID, PASSWORD)

        for _ in range(20):  
            if wlan.isconnected():
                print("✅ Conectado a Wi-Fi!")
                print("📡 Dirección IP:", wlan.ifconfig()[0])
                return wlan
            blink_led(1, 0.5)  

        print("❌ No se pudo conectar al Wi-Fi.")
        return None
    return wlan

