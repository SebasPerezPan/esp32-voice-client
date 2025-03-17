import machine
import os
from setup import sdcard

SD_MOUNT_POINT = "/sd"

def mounting_sd():
    """Inicializa y monta la tarjeta SD en /sd si no está montada"""
    spi = machine.SPI(1, baudrate=1000000, polarity=0, phase=0, 
                      sck=machine.Pin(18), mosi=machine.Pin(23), miso=machine.Pin(19))
    cs = machine.Pin(5, machine.Pin.OUT)

    try:
        if "/sd" not in os.listdir("/"):
            sd = sdcard.SDCard(spi, cs)
            vfs = os.VfsFat(sd)
            os.mount(vfs, "/sd")
            print("✅ SD montada automáticamente en /sd")

            # Crear carpetas si no existen
            dirs = ["/sd/home", "/sd/home/serverAnswer", "/sd/home/serverRequest", "/sd/home/intSounds"]
            for d in dirs:
                try:
                    os.mkdir(d)
                except OSError:
                    pass  # La carpeta ya existe
        else:
            print("ℹ️ SD ya estaba montada")
    except Exception as e:
        print("❌ Error montando la SD:", str(e))

# Ejecutar la inicialización al importar

def init():
    """Verifica si la SD está montada, si no, la monta."""
    try:
        os.listdir(SD_MOUNT_POINT)  # Intentar acceder a la SD
        print("ℹ️ SD ya estaba montada")
    except OSError:
        mounting_sd()

