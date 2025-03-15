from machine import I2S, Pin

I2S_ID = 0  # Puede ser 0 o 1 en el ESP32
BCLK_PIN = 22  # Bit Clock (SCK)
WS_PIN = 19    # Word Select (L/R Clock)
DATA_IN_PIN = 23  # Serial Data (SD)

def init_mic():
    """Inicializa el micrófono I2S para grabación"""
    audio_in = I2S(
        I2S_ID,
        sck=Pin(BCLK_PIN),
        ws=Pin(WS_PIN),
        sd=Pin(DATA_IN_PIN),
        mode=I2S.RX,
        bits=16,
        format=I2S.MONO,
        rate=16000,
        ibuf=40000  # Buffer de 40 KB
    )
    return audio_in

