import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from nlutils.Utils.Log import default_logger

from Configure import AIWConfigure



class EmailManager(object):

    def __new__(cls,*args,**kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EmailManager, cls).__new__(cls, *args, **kwargs)
        return cls.instance
    
    def connect(self):
        sender_address = AIWConfigure.get_instance().get_config_info("ServerEmailAddress").as_string()
        sender_crediential = AIWConfigure.get_instance().get_config_info("QQCrediential").as_string()
        self.sender_address = sender_address
        self.proxy = smtplib.SMTP_SSL('smtp.qq.com', smtplib.SMTP_SSL_PORT)
        self.proxy.login(sender_address, sender_crediential)
    
    def __init__(self):
        while True:
            try:
                self.connect()
                default_logger.info(f'Connect QQ SMTP Server successfully')
                return
            except Exception as e:
                default_logger.error(f'Error connecting to QQ SMTP Server: {e.__str__()}, retrying...')
    
    def create_pkg(self, destination, msg, subject):
        pkg = MIMEText(msg, 'plain', 'utf-8')
        pkg['From'] = self.sender_address
        pkg['To'] = destination
        pkg['Subject'] = subject
        return pkg

    def send_to(self, destination, msg, subject):
        msg = self.create_pkg(destination, msg, subject)
        try:
            self.proxy.sendmail(self.sender_address, destination, msg.as_string())
        except smtplib.SMTPException as e:
            default_logger.error("Error sending email")

    def __del__(self):
        self.proxy.close()

if __name__ == '__main__':
    man = EmailManager()
    man.send_to('mliu444@gatech.edu', 'Test Message', 'Test Subject')