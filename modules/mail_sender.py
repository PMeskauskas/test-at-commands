from email.message import EmailMessage
import smtplib


class MailSender:
    def __init__(self):
        self.msg = EmailMessage()

    def form_message_success(self, destination, device_name):

        self.msg['From'] = 'stalozaidimudalinimasis@outlook.com'
        self.msg['To'] = destination
        self.msg['Subject'] = 'The program was tested successfully!'
        self.msg.set_content('''
        <!DOCTYPE html>
        <html>
            <body>

                <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;">
                    The tested device {0} finished without interruptions.
                </h2>

            </body>
        </html>
        '''.format(device_name), subtype='html')

    def form_message_failed(self, destination, device_name):
        self.msg['From'] = 'stalozaidimudalinimasis@outlook.com'
        self.msg['To'] = destination
        self.msg['Subject'] = 'The program has failed!'
        self.msg.set_content('''
        <!DOCTYPE html>
        <html>
            <body>

                <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;">
                    The tested device {0} failed while testing.
                </h2>

            </body>
        </html>
        '''.format(device_name), subtype='html')

    def send_mail(self):
        try:

            mailserver = smtplib.SMTP('smtp.office365.com', 587)
            mailserver.ehlo()
            mailserver.starttls()

            try:
                mailserver.login('stalozaidimudalinimasis@outlook.com',
                                 'gqjcfxntqitshslo')
                mailserver.send_message(self.msg)
            finally:
                mailserver.quit()
        except:
            pass
