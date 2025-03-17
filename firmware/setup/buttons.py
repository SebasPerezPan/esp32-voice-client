import machine
import time
import _thread
from modes import state

# Lista de pines asignados a los botones
BUTTON_PINS = [32, 33, 14, 25, 27]  

# Diccionario para almacenar objetos de los botones
buttons = {}

# Variable de bloqueo para evitar múltiples activaciones en 2 segundos
last_press_time = 0
lock = _thread.allocate_lock()

def button_pressed(pin_obj):
    """Maneja la pulsación de un botón"""
    global last_press_time

    pin_number = BUTTON_PINS[[buttons[p] for p in BUTTON_PINS].index(pin_obj)]


    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_press_time) < 2000:
        return  # Ignora si se presiona antes de 2 segundos

    last_press_time = current_time
    _thread.start_new_thread(disable_buttons, ())

    if state.recording:
        print(f"🛑 Botón en GPIO{pin_number} presionado. Deteniendo grabación...")
        _stop_recording()
    else:
        print(f"🎤 Botón en GPIO{pin_number} presionado. Iniciando grabación...")
        _start_recording()


def _stop_recording():
    """Llama a sent_mode para detener la grabación"""
    from modes import sent_mode  # 🔹 Importación dentro de función para evitar ciclos
    sent_mode.mic.stop_recording()
    state.recording = False

def _start_recording():
    """Llama a sent_mode para iniciar la grabación"""
    from modes import sent_mode  # 🔹 Importación dentro de función para evitar ciclos
    sent_mode.sent_mode()

def disable_buttons():
    """Bloquea los botones temporalmente"""
    with lock:
        time.sleep(2)  # Bloqueo de 2 segundos

def setup_buttons():
    """Configura los botones con interrupciones"""
    for pin in BUTTON_PINS:
        buttons[pin] = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        buttons[pin].irq(trigger=machine.Pin.IRQ_FALLING, handler=lambda p: button_pressed(p))
    print("✅ Botones configurados correctamente.")



