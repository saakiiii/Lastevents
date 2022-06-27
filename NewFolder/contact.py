from email.mime.text import MIMEText
from GmailApi import GmailSend

class Contactemail:
     
     def __init__(self) -> None:
        # self.from_email = "dummyjoi710@gmail.com"
        # self.password = "lenovag40"
        pass
          
     def email(self, email, message): 
            cfr = f"""
                 From:{email}
                 Message:{
                     message
                 }
            """
            msg = cfr
            val = GmailSend().send_email(msg=msg, to="saakiiikas@gmail.com", subject="FEEDBACK-CONTACT")
            # msg = MIMEText(message)
            # msg["Subject"] = "Reset Password-fourlinenews"
            # msg["From"] = "dummyjoi710@gmail.com"
            # msg["To"] = "saakii574@gmail.com"
            print(val)
            return True
        