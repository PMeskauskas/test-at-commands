import ftplib


class FTPUpload:
    def __init__(self, filename, server_data):
        self.filename = filename
        self.server_data = server_data
        self.file = None
        self.ftp_session = None
        self.open_ftp_session()
        self.open_ftp_file()
        self.store_ftp_file()
        self.close_ftp()

    def open_ftp_session(self):
        try:
            self.ftp_session = ftplib.FTP(
                host=self.server_data['hostname'], user=self.server_data['username'], passwd=self.server_data['password'])

        except:
            print('Failed to create FTP session')
            exit(1)

    def open_ftp_file(self):
        try:
            self.file = open(f'results/{self.filename}', 'rb')

        except FileNotFoundError:
            print("File not found for FTP transfer")
            self.ftp_session.quit()
            exit(1)

    def store_ftp_file(self):
        try:
            store_command = f"STOR {self.filename}"
            self.ftp_session.storbinary(store_command, self.file)
        except:
            print("Could not transfer file to FTP server")
            self.close_ftp(self)
            exit(1)

    def close_ftp(self):
        self.file.close()
        self.ftp_session.quit()
