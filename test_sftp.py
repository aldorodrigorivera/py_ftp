import ftplib
import json
import base64
from datetime import datetime

# Configuración del servidor FTP
ftp_host = 'f...'
ftp_user = 'M...'
ftp_password = 'A...'

# Establecer conexión FTP
ftp = ftplib.FTP(ftp_host)
ftp.login(ftp_user, ftp_password)

# Directorio remoto
remote_dir = '/RECEIVE'

# Obtener lista de archivos en el directorio remoto
file_list = ftp.nlst(remote_dir)

# Filtrar archivos por fecha
filtered_files = []
target_date = datetime(2023, 10, 10)  # Fecha objetivo

for file_name in file_list:
    file_date = ftp.sendcmd('MDTM ' + file_name)[4:]
    file_date = datetime.strptime(file_date, '%Y%m%d%H%M%S')
    if file_date.date() == target_date.date():
        filtered_files.append(file_name)
print("FILTERED",filtered_files)


# Leer el contenido de los archivos y crear el JSON de salida
output = []

for file_name in filtered_files:
    file_content=''
    with open(file_name, "rb") as file:
            # Leer el contenido del archivo en bytes
            content = file.read()

            # Codificar en Base64
            content_codificado = base64.b64encode(content)

            # Decodificar los bytes codificados en una cadena
            file_content = content_codificado.decode('utf-8')

            file_content
    # file_content_bytes = ftp.retrbinary('RETR ' + file_name, lambda data: None).encode('utf-8')
    # file_content = base64.b64encode(file_content_bytes).decode('utf-8')
    file_info = {'file_name': file_name, 'file_content': file_content}
    output.append(file_info)

print(output)
# Cerrar la conexión FTP
ftp.quit()

# Generar el JSON de salida
json_output = json.dumps(output, indent=4)
print(json_output)