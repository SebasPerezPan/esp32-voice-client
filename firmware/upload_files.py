import os
import subprocess

# Ruta de la carpeta local que quieres cargar
local_folder = "setup"
# Puerto del ESP32
port = "/dev/ttyUSB0"

# Recorrer todos los archivos de la carpeta y cargarlos
for root, dirs, files in os.walk(local_folder):
    for file in files:
        local_path = os.path.join(root, file)
        remote_path = os.path.join("/setup", os.path.relpath(local_path, local_folder)).replace("\\", "/")  # Ajustar ruta
        subprocess.run(["ampy", "--port", port, "put", local_path, remote_path])

