from EmailApi import SendEmail

class Contactemail:
     
     def __init__(self) -> None:
        pass
          
     def email(self, email, message): 
            cfr = f"""
                 From:{email}
                 Message:{
                     message
                 }
            """
            msg = cfr
            val = SendEmail().send_email(msg=msg, to="contact@lastevents.space", subject="FEEDBACK-CONTACT")            
            return True
        