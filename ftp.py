from ftplib import FTP
from datetime import datetime
import base64

ftp_server = 'ftp.p....'
ftp_user = 'M....'
ftp_password = 'A....'
ftp_directory = '/RECEIVE'
date_threshold = datetime(2023, 10, 10) 

def list_files_by_date(ftp, date_threshold):
    files = []
    ftp.retrlines('LIST', files.append)
    
    filtered_files = []

    for line in files:
        parts = line.split()
        if len(parts) < 9:
            continue
        
        file_name = parts[-1]
        file_date_str = ftp.sendcmd('MDTM ' + file_name)[4:]
        file_date = datetime.strptime(file_date_str, '%Y%m%d%H%M%S')

        if file_date >= date_threshold:
            filtered_files.append(file_name)

    return filtered_files

def download_files(ftp, files):
    for file_name in files:
        with open(f"./temp/temp_edi.txt", 'wb') as local_file:
            ftp.retrbinary('RETR ' + file_name, local_file.write)
            print(f"Downloaded: {file_name}")

def read_file(ftp, files):
    output = []
    for file_name in files:
        file_content=''
        with open(file_name, "rb") as file:
                content = file.read()
                content_codificado = base64.b64encode(content)
                file_content = content_codificado.decode('utf-8')
                file_content
        file_info = {'file_name': file_name, 'file_content': file_content}
        output.append(file_info)
    return output

def main():
    try:
        ftp = FTP(ftp_server)
        ftp.login(ftp_user, ftp_password)
        ftp.cwd(ftp_directory)

        filtered_files = list_files_by_date(ftp, date_threshold)
        download_files(ftp, filtered_files)
        json = read_file(ftp, ['./temp/temp_edi.txt'])
        print("JSON::::", json)

        ftp.quit()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
