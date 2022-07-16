import smtplib

from sqlalchemy import true

class SendEmail:
    
    def __init__(self) -> None:
        pass
    
    def send_email(self, msg, to, subject):
        subject = f"Subject: {subject} \n\n"
        msg = msg+'\n\n'
        connection = smtplib.SMTP_SSL('smtp.zoho.in', 465) 
        connection.ehlo()
        connection.login("help@lastevents.space", "106PAvNJgTfy")
        connection.sendmail(msg=subject+msg, from_addr="help@lastevents.space", to_addrs=to)
        connection.quit()
        return True
