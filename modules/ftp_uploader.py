import ftplib


class FTPUploader:
    def __init__(self, *args, **kwargs):
        self.file = None
        self.ftp_session = None

    def open_ftp_session(self, server_data):
        try:
            self.ftp_session = ftplib.FTP(
                host=server_data['hostname'],
                user=server_data['username'],
                passwd=server_data['password'])

        except:
            exit('Failed to create FTP session')

    def open_ftp_file(self, filename):
        try:
            self.file = open(f'results/{filename}', 'rb')

        except FileNotFoundError:
            self.ftp_session.quit()
            exit("File not found for FTP transfer")

    def store_ftp_file(self, filename):
        try:
            store_command = f"STOR {filename}"
            self.ftp_session.storbinary(store_command, self.file)
        except:
            self.close_ftp(self)
            exit("Could not transfer file to FTP server")

    def close_ftp(self):
        self.file.close()
        self.ftp_session.quit()
