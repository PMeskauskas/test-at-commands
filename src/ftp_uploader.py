import ftplib


class FTPUploader:
    def __init__(self, *args, **kwargs):
        self.file = None
        self.ftp_session = None

    def open_ftp_session(self, hostname, username, password):
        try:
            self.ftp_session = ftplib.FTP(
                host=hostname, user=username, passwd=password)

        except:
            print('Failed to create FTP session')
            exit(1)

    def open_ftp_file(self, filename):
        try:
            self.file = open(f'results/{filename}', 'rb')

        except FileNotFoundError:
            print("File not found for FTP transfer")
            self.ftp_session.quit()
            exit(1)

    def store_ftp_file(self, filename):
        try:
            store_command = f"STOR {filename}"
            self.ftp_session.storbinary(store_command, self.file)
        except:
            print("Could not transfer file to FTP server")
            self.close_ftp(self)
            exit(1)

    def close_ftp(self):
        self.file.close()
        self.ftp_session.quit()
