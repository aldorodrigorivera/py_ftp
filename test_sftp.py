import ftplib
import json
import base64
from datetime import datetime

ftp_host = 'f...'
ftp_user = 'M...'
ftp_password = 'A...'

ftp = ftplib.FTP(ftp_host)
ftp.login(ftp_user, ftp_password)

remote_dir = '/RECEIVE'

file_list = ftp.nlst(remote_dir)

filtered_files = []
target_date = datetime(2023, 10, 10)

for file_name in file_list:
    file_date = ftp.sendcmd('MDTM ' + file_name)[4:]
    file_date = datetime.strptime(file_date, '%Y%m%d%H%M%S')
    if file_date.date() == target_date.date():
        filtered_files.append(file_name)
print("FILTERED",filtered_files)

output = []

for file_name in filtered_files:
    file_content=''
    with open(file_name, "rb") as file:
            content = file.read()

            content_codificado = base64.b64encode(content)

            file_content = content_codificado.decode('utf-8')

            file_content
    file_info = {'file_name': file_name, 'file_content': file_content}
    output.append(file_info)

print(output)
ftp.quit()

json_output = json.dumps(output, indent=4)
print(json_output)