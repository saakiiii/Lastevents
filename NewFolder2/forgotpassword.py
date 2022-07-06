import requests
import json
import bcrypt
from EmailApi import SendEmail

from codegenerator import codeId

class ResetPassword:

    def __init__(self):
        # self.from_addr_ = "dummyjoi710@gmail.com"
        # self.to_addrs = "saakii574@gmail.com"
        self.findone = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/findOne"
        self.updateone = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/updateOne"
        self.insertone = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/insertOne"
        self.deleteone = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/deleteOne"
        self.find = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/find"
        self.header = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': "UOGuFyCP3TfwSzHGQo1aOOU5Q5OQK7xPK3xlLsY6T2EWo8WKYxzD7AagtMYAtpY2",
        }

    def sendresetpasswordmail(self, email):
    #    try:
        # keys = self.collection.find_one({"id":"keys"}, {"keys"})["keys"]
        key = codeId().generate_password_reset_key()
        message = f"""

            www.lastevents.space
            Click this link to change your password,
                   https://www.lastevents.space/resetpassword?key={key}

            """
        val = SendEmail().send_email(msg=message, to=email, subject="Forgot Password | lastevents.space")
        payload = json.dumps({
                    "collection": "resets",
                    "database": "newsmain",
                    "dataSource": "Cluster0",
                    "document":{
                        "email":email,
                        "key":key
                    }
                })
        response = requests.request("POST", self.insertone, headers=self.header, data=payload)
        print(response.text)
        return True

    def resetpassword(self, newpassword, key):
            print(key)
            payload0 = json.dumps({
                        "collection": "resets",
                        "database": "newsmain",
                        "dataSource": "Cluster0",
                        "filter":{
                            "key":key
                        }
                    })
            email =   requests.request("POST", self.findone, headers=self.header, data=payload0).json()
            print(email)
            if email["document"] is None:
                return "Link Expired"
            email = email["document"]["email"]
            password = bcrypt.hashpw(newpassword.encode(), bcrypt.gensalt()).decode()
            # password = newpassword
            payload1 = json.dumps({
                    "collection": "users",
                    "database": "newsmain",
                    "dataSource": "Cluster0",
                    "filter":{
                        "email":email
                        },
                    "update":{
                        "$set":{
                            "password":password
                        }
                    }
                })
            requests.request("POST", self.updateone, headers=self.header, data=payload1)
            payload2 = json.dumps({
                    "collection": "resets",
                    "database": "newsmain",
                    "dataSource": "Cluster0",
                    "filter":{
                        "key":key,
                        "email":email
                    }
                })
            requests.request("POST", self.deleteone, headers=self.header, data=payload2)

            # self.collection1.update_one({"email":email}, {"$set":{"password":newpassword}})
            # self.collection.delete_one({"key":key})
            return {"email":email,
                    "password":password}
        # except:
        #     pass


