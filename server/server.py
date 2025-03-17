import socket
import os
import subprocess
from pydub import AudioSegment
from io import BytesIO

# Configuración
HOST = "0.0.0.0"  # Acepta conexiones de cualquier IP
PORT = 5000
WAV_FILE = "received.wav"
MP3_FILE = "received.mp3"

def save_audio(data, filename):
    """Guarda los datos recibidos en un archivo"""
    with open(filename, "wb") as f:
        f.write(data)
    print(f"Archivo {filename} guardado correctamente.")

def is_valid_wav(filename):
    """Verifica si el archivo WAV no está corrupto"""
    try:
        audio = AudioSegment.from_wav(filename)
        return True
    except Exception as e:
        print("Archivo WAV corrupto:", e)
        return False

def convert_wav_to_mp3(input_wav, output_mp3):
    """Convierte un archivo WAV a MP3 usando FFmpeg"""
    command = ["ffmpeg", "-i", input_wav, "-codec:a", "libmp3lame", "-b:a", "128k", output_mp3, "-y"]
    subprocess.run(command, check=True)
    print(f"Convertido a {output_mp3}")

def handle_client(conn):
    """Maneja la conexión con el cliente"""
    print("Cliente conectado")
    
    data = b""
    while True:
        chunk = conn.recv(1024)
        if not chunk or b"EOF" in chunk:  # EOF indica fin de archivo
            break
        data += chunk
    
    conn.close()
    
    if len(data) < 44:  # Un archivo WAV mínimo tiene un header de 44 bytes
        print("Error: Archivo recibido demasiado pequeño.")
        return
    
    save_audio(data, WAV_FILE)

    if is_valid_wav(WAV_FILE):
        convert_wav_to_mp3(WAV_FILE, MP3_FILE)
        print(f"Archivo MP3 listo: {MP3_FILE}")
        os.remove(WAV_FILE)  # Borra el WAV después de la conversión
    else:
        print("El archivo WAV es inválido. No se convierte.")

def start_server():
    """Inicia el servidor TCP"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Servidor escuchando en {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"Conexión desde {addr}")
        handle_client(conn)

if __name__ == "__main__":
    start_server()
