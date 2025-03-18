import os
import time
import websocket
from modes import idle_mode, state
from setup import mic  # Importamos la configuración del micrófono

def sent_mode(sock=None):  # 🔹 Permitimos que el socket sea opcional
    if sock is None:
        sock = state.sock  # 🔹 Lo tomamos de state si no se pasó
        print("🔴 Iniciando grabación...")

    # Actualizar estado global
    state.recording = True  

    file_path = "/sd/home/serverRequest/audioRequest.wav"
    
    # Inicializar micrófono
    microphone = mic.init_mic()
    
    # Tamaño del buffer
    buffer_size = 4096  # Ajusta el tamaño según la memoria disponible
    audio_buffer = bytearray(buffer_size)

    # Crear archivo WAV
    try:
        with open(file_path, "wb") as f:
            print("⏺ Grabando audio...")

            start_time = time.time()

            while state.recording:  # Se graba mientras state.recording sea True
                # Leer datos del micrófono al buffer y escribir en el archivo
                num_bytes = microphone.readinto(audio_buffer)
                if num_bytes:
                    f.write(audio_buffer[:num_bytes])
                
                # Parar grabación si se alcanza el tiempo máximo
                if time.time() - start_time >= 90:
                    print("⏳ Tiempo límite alcanzado. Deteniendo grabación...")
                    state.recording = False  # Actualizamos el estado para que otros módulos lo vean

                time.sleep(0.1)  # Pequeño delay para evitar sobrecarga de CPU

        print(f"💾 Archivo guardado en {file_path}")
    
    except Exception as e:
        print(f"❌ Error durante la grabación: {e}")
        state.recording = False
        microphone.deinit()  # Liberar el micrófono
        idle_mode.idle_mode(sock)
        return

    state.recording = False  # 🔹 Detener el estado de grabación

    # Enviar el archivo al servidor
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            #deprecado, porfavor utilizar la libreria requests y de una vez guardar el archivo de audio en este punto del codigo atravez de una solicitud post al backend
            #sock.send(data)
        
        print("📤 Archivo enviado al servidor.")

        # Eliminar el archivo solo si se envió correctamente
        os.remove(file_path)
        print("🗑 Archivo eliminado.")
        
    except Exception as e:
        print(f"❌ Error enviando el archivo: {e}")
        print("🔄 Regresando a modo idle.")
        microphone.deinit()  # Liberar el micrófono antes de salir
        #siento que esto puede generar un problema de memorly leak, siendo que idle mode ya esta corriendo
        idle_mode.start(sock)
        return

    # Transición a received_mode
    print("📥 Cambiando a modo recepción...")
    microphone.deinit()  # Liberar el micrófono antes de cambiar de modo
    received_mode.start(sock)


