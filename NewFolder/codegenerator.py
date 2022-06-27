import string
import random
import datetime
import json
import requests

class codeId:

    def __init__(self):
        self.findone = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/findOne"
        self.updateone = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/updateOne"
        self.header = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': "UOGuFyCP3TfwSzHGQo1aOOU5Q5OQK7xPK3xlLsY6T2EWo8WKYxzD7AagtMYAtpY2",  
        }
        payload = json.dumps({
            "collection": "ids",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "id":"data"
            }
        })

        response = requests.request("POST", self.findone, headers=self.header, data=payload).json()
        # self.ids = response["document"]["ids"]
        # self.keys = response["document"]["keys"]
        self.ids = []
        self.keys = []

    def generate_id(self):
        code_ = None
        x = 100
        while True:
            endnum = 99999+len(self.ids)+x
            ascii_letters = string.ascii_letters
            number = random.randint(10000, endnum)
            letters = [ascii_letters[i] for i in range(len(ascii_letters))]
            random.shuffle(letters)
            random_letters = letters[:5]
            time = datetime.datetime.now().strftime("%H:%M:%S").split(':')
            random_letters.extend(time)
            first_half = "".join(random_letters)
            code = first_half+str(number)
            if code not in self.ids:
                code_ = code
                newsarticle = json.dumps({
                        "collection": "ids",
                        "database": "newsmain",
                        "dataSource": "Cluster0",
                        "filter":{
                            "id":"data"
                        },
                        "update":{
                            "$push":{
                                "ids":code_
                            }
                        }
                        })
                response = requests.request("POST", url=self.updateone, headers=self.header, data=newsarticle)
                print("code", response.text)
                return code_
            else:
                x += 100

    def generate_password_reset_key(self):
        keys = self.keys
        code_ = None
        x = 100
        while True:
            endnum = 999999+x
            ascii_letters = string.ascii_letters
            number = random.randint(100000, endnum)
            num_str = str(number)
            letters = [ascii_letters[i] for i in range(len(ascii_letters))]
            nums = [num_str[i] for i in range(len(num_str))]
            random_letters = letters[:15]
            time = datetime.datetime.now().strftime("%H:%M:%S").split(':')
            random_letters.extend(time)
            random_letters.extend(nums)
            random.shuffle(random_letters)
            first_half = "".join(random_letters)
            code = first_half+str(number)
            if code not in keys:
                code_ = code
                break
            else:
                x += 1000
        return code_
    
    def generate_verify_code(self):
        return random.randint(10000, 100000)