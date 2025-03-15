import os
import time
import setup_server  # Para gestionar la conexión con el servidor
import idle_mode  # Para volver a modo reposo si no hay archivos
# from setup_audio import play_audio  # Función para reproducir audio

def received_mode():
    server_folder = "sd/home/serverAnswer/"
    max_wait_time = 60  # 1 minuto máximo
    check_interval = 2  # Revisar cada 2 segundos
    elapsed_time = 0

    print("🟢 Modo recepción activo. Esperando archivo...")

    while elapsed_time < max_wait_time:
        print("🔍 Buscando archivos...")
        files = os.listdir(server_folder)
        
        if files:
            filename = files[0]  # Tomamos el primer archivo recibido
            file_path = os.path.join(server_folder, filename)
            
            print(f"✅ Se recibió: {filename}")
            play_audio(file_path)  # Reproducimos el audio
            print(f"▶️ Reproduciendo: {filename}")
            
            os.remove(file_path)  # Eliminamos el archivo después de reproducirlo
            print(f"🗑 Archivo eliminado: {filename}")
            
            idle_mode.start()  # Volver a modo reposo
            return  # Salir de received_mode

        time.sleep(check_interval)
        elapsed_time += check_interval
    
    print("⏳ Tiempo de espera agotado. Volviendo a modo reposo.")
    idle_mode.start()  # Si no llega archivo en 1 minuto, volver a reposo

