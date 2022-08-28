import json
import re
from urllib.parse import uses_relative
import requests
from CoStCi import CountriesStatesCities
from awsbucket import AwsS3
from codegenerator import codeId
import datetime
import bcrypt
from EmailApi import SendEmail
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import base64
import os

class BackEnd:

    def __init__(self) -> None:
        self.findone = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/findOne"
        self.updateone = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/updateOne"
        self.update = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/updateMany"
        self.insertone = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/insertOne"
        self.deleteone = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/deleteOne"
        self.find = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/find"
        self.delete = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/deleteMany"
        self.header = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': "UOGuFyCP3TfwSzHGQo1aOOU5Q5OQK7xPK3xlLsY6T2EWo8WKYxzD7AagtMYAtpY2",
        }

    # SIGN IN AND REGISTER

    def create_user(self,
                    username,
                    email,
                    password,
                    country,
                    state,
                    city):
        user_id = codeId().generate_id()
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        newuser = {
            "email":email,
            "user_id":user_id,
            "username":username,
            "password":password,
            "country":country,
            "state":state,
            "city":city,
            "contributions":0,
            "total_articles":0,
            "today_total_articles":0,
            "total_views":0,
            "today_total_views":0,
            "total_earning":0,
            "today_total_blog_articles":0,
            "total_blog_articles":0,
            "total_blog_view":0,
            "today_total_blog_views":0,
            "today_total_income":0,
            "last_month_earning":0,
            "data_joined":datetime.datetime.now().strftime("%d-%m-%Y"),
            "verify_id":'',
            "verified":0
        }
        newdata = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "document" : newuser
            })

        response = requests.request("POST", url=self.insertone, headers=self.header, data=newdata)
        self.setNotification(user_id=user_id, notify_msg="Welcome to lastevents.space, explore and keep you updated")
        SendEmail().send_email(msg=f"{username} has signed up", to="admin@lastevents.space", subject="New User")
        return {"user_id":user_id, "password":password}

    # VALIDITY

    def validemail(self, email):
        email_ = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "email":email
                }
            })
        response = requests.request("POST", url=self.findone, headers=self.header, data=email_)
        email__ = response.json()["document"]
        if email__ == None:
            return True
        else:
            return False

    def validpassword(self, password):
        if len(password) >= 8:
            return True
        else:
            return False

    def validemail_and_password_for_login(self, email, password):
        password_ = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "email":email
                }
            })
        response = requests.request("POST", url=self.findone, headers=self.header, data=password_)
        password_ = response.json()["document"]["password"]
        if bcrypt.checkpw(password.encode(), password_.encode()):
            return True
        else:
            return False


    def validusername(self, username):
        username_ = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "username":username
                }
            })
        response = requests.request("POST", url=self.findone, headers=self.header, data=username_)
        username__ = response.json()["document"]
        if username__ == None:
            return True
        else:
            return False

    def validheadingurls(self, heading_url):
        heading_url__ = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "heading_url":heading_url
                }
            })
        response = requests.request("POST", url=self.findone, headers=self.header, data=heading_url__)
        heading_urls = response.json()["document"]
        if heading_urls == None:
            heading_url__ = json.dumps({
                "collection": "blogarticles",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "heading_url":heading_url
                    }
                })
            response = requests.request("POST", url=self.findone, headers=self.header, data=heading_url__)
            heading_urls = response.json()["document"]
            if heading_urls == None:
                return True
        else:
            return False

    def user_articles_revenue_data(self, user_id):
        user_data_ = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
                }
            })
        response = requests.request("POST", url=self.findone, headers=self.header, data=user_data_)
        result = {  "total_articles" : response.json()["document"]["total_articles"],
                    "today_total_aritcles" : response.json()["document"]["today_total_articles"],
                    "total_views" : response.json()["document"]["total_views"],
                    "today_total_views" : response.json()["document"]["today_total_views"],
                    "total_earning" : response.json()["document"]["total_earning"],
                    "today_total_income" : response.json()["document"]["today_total_income"],
                    "last_month_earning" : response.json()["document"]["last_month_earning"]
        }
        return result

    # WRITE (NEWS)

    def news_article_write(self,
                           heading,
                           author_id,
                           author_name,
                           news,
                           country,
                           category,
                           state,
                           city='',
                           keywords=[],
                           views=0,
                           perm_une_='',
                           perm_='') -> bool:

        news_id = codeId().generate_id()
        heading_url = re.sub(r'[@_!#$%^&*()<>?/\|}{~:]', "", heading)
        heading_url = heading_url.replace(" ", "-")
        if heading_url[-1] == '.':
            heading_url = heading_url[0:-1]
        heading_url = GoogleTranslator(source='auto', target='en').translate(heading_url)
        if not self.validheadingurls(heading_url):
            # return "Invalid heading"
            heading_url = heading_url + "-"
        replaced_str = re.sub('[/<\/?^>+(>|$)/g]', "", news)
        total_words = len(replaced_str.split(" "))
        news = self.image_processing_and_uploading(news)
        newsarticle = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "document" : {
                 "heading":heading,
                 "heading_url":heading_url,
                 "news_id":news_id,
                 "author":author_name,
                 "date":datetime.datetime.now().strftime("%d-%m-%Y"),
                 "time":datetime.datetime.now().strftime("%H:%M"),
                 "author_id":author_id,
                 "news":news,
                 "read_time":str(total_words/200).split('.')[0],
                 "category":category,
                 "country":country,
                 "state":state,
                 "city":city,
                 "keywords":keywords,
                 "views":views,
                 "reports":[],
                 "can_display_une":perm_une_,
                 "article_length":len(replaced_str),
                 "total_words":total_words
            }
        })

        response = requests.request("POST", url=self.insertone, headers=self.header, data=newsarticle)
        data = self.get_user_instance(user_id=author_id)
        self.setNotification(user_id=author_id, notify_msg= f"{heading} - uploaded successfully")
        if perm_ == '1':
         recents = json.dumps({
            "collection": "recents",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "document":{
                 "heading_url":heading_url,
                 "id":"data",
                 "type":"news",
            }
            })
         response = requests.request("POST", url=self.insertone, headers=self.header, data=recents)
        return True

    # WRITE (BLOG)

    def blogs_article_write(self,
                           heading,
                           author_id,
                           author_name,
                           blog,
                           perm_,
                           keywords=[],
                           views=0,
                           ) -> bool:

        blogs_id = codeId().generate_id()
        heading_url = re.sub(r'[@_!#$%^&*()<>?/\|}{~:]', "", heading)
        heading_url = heading_url.replace(" ", "-")
        if heading_url[-1] == '.':
            heading_url = heading_url[0:-1]
        heading_url = GoogleTranslator(source='auto', target='en').translate(heading_url)
        if not self.validheadingurls(heading_url):
            # return "Invalid heading"
            heading_url = heading_url + "-"
        replaced_str = re.sub('[/<\/?^>+(>|$)/g]', "", blog)
        total_words = len(replaced_str.split(" "))
        blog = self.image_processing_and_uploading(blog)
        blogarticle = json.dumps({
            "collection": "blogarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "document" : {
                 "heading":heading,
                 "heading_url":heading_url,
                 "blog_id":blogs_id,
                 "author":author_name,
                 "description":blog[0:70]+"...",
                 "date":datetime.datetime.now().strftime("%d-%m-%Y"),
                 "time":datetime.datetime.now().strftime("%H:%M"),
                 "author_id":author_id,
                 "blog":blog,
                 "read_time":str(total_words/200).split('.')[0],
                 "keywords":keywords,
                 "views":views,
                 "reports":[],
                 "article_length":len(replaced_str),
                 "total_words":total_words
            }
        })

        response = requests.request("POST", url=self.insertone, headers=self.header, data=blogarticle)
        self.setNotification(user_id=author_id, notify_msg= f"{heading} - uploaded successfully")
        if perm_ == '1':
         recents = json.dumps({
            "collection": "recents",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "document":{
                 "heading_url":heading_url,
                 "id":"data",
                 "type":"blog",
            }
            })
         response = requests.request("POST", url=self.insertone, headers=self.header, data=recents)
        return True

    # USER

    def calculate_user_contribution(self, user_id):
        newsarticle = len(self.get_users_articles(user_id=user_id))
        blogarticle = len(self.get_users_blog_article(user_id=user_id))
        comments = len(self.getCommentsofUser(user_id=user_id))
        meorops = len(self.get_opinions_of_user(user_id=user_id))
        contributions = (newsarticle * 10) + (blogarticle * 10) + (comments * 3) + (meorops * 7)
        return contributions

    def get_user_by_username(self, username):
        user_instance = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "username":username
            }
        })
        response = requests.request("POST", url=self.findone, headers=self.header, data=user_instance).json()["document"]
        return response

    def get_user_instance(self, user_id):
        user_instance = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
            }
        })
        response = requests.request("POST", url=self.findone, headers=self.header, data=user_instance).json()["document"]
        return response

    def update_profile(self, user_id, username, country, state):
        updateuser = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
            },
            "update":{
                "$set":{
                    "username":username,
                    "country":country,
                    "state":state
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=updateuser)
        return True

    def update_user_name(self, user_id, newusername, prev_username):
        updateuser = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
            },
            "update":{
                "$set":{
                    "username":newusername
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=updateuser)
        return True

    def update_user_country(self, user_id, country):
        updateuser = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
            },
            "update":{
                "$set":{
                    "country":country
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=updateuser)
        return True

    def update_user_state(self, user_id, state):
        updateuser = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
            },
            "update":{
                "$set":{
                    "state":state
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=updateuser)
        return True

    def update_user_city(self, user_id, city):
        updateuser = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
            },
            "update":{
                "$set":{
                    "city":city
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=updateuser)
        return True


    # INCREMENT AND DECREMENT

    def increment_total_news_article_views(self, user_id):
        data = self.get_user_instance(user_id)
        total_views = data["total_views"]
        user_id = data["user_id"]

        articles_count_data = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
            },
            "update":{
                "$set":{
                   "total_views":total_views+1
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=articles_count_data)
        return "Added"

    def increment_total_blog_article_views(self, user_id):
        data = self.get_user_instance(user_id)
        total_blog_view = data["total_blog_view"]
        user_id = data["user_id"]

        articles_count_data = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
            },
            "update":{
                "$set":{
                   "total_blog_view":total_blog_view+1
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=articles_count_data)
        return "Added"


    def increment_page_views(self, heading_url, val):
        article_instance = self.getarticle_instance(heading_url=heading_url, val=val)
        article = json.dumps({
            "collection": val,
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "heading_url":heading_url
            },
            "update":{
                "$set":{
                    "views":article_instance["views"]+1
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=article)
        user_id = self.get_user_by_article(heading_url=heading_url, val=val)
        if val == "newsarticles":
           self.increment_total_news_article_views(user_id=user_id)
        if val == "blogarticles":
            self.increment_total_blog_article_views(user_id=user_id)
        return True

    # GET NEWS

    def news_get(self, country, state, category, city):
        newsarticles = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "country":country,
                "state":state,
                "category":category,
                "city":city
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=newsarticles)
        data_in_list = response.json()["documents"]
        data_in_list.reverse()

        newsarticles_1 = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "country":country,
                "state":state,
                "category":category
            }
        })
        response_1 = requests.request("POST", url=self.find, headers=self.header, data=newsarticles_1)
        data_in_list_1 = response_1.json()["documents"]
        data_in_list_1.reverse()
        for i in data_in_list_1:
            if i not in data_in_list:
                data_in_list.append(i)
        # data_in_list.extend(data_in_list_1)
        # data_in_list = list(set(data_in_list))

        newsarticles_2 = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "country":country,
                "state":state,            }
        })
        response_2 = requests.request("POST", url=self.find, headers=self.header, data=newsarticles_2)
        data_in_list_2 = response_2.json()["documents"]
        data_in_list_2.reverse()
        for i in data_in_list_2:
            if i not in data_in_list:
                data_in_list.append(i)
        # data_in_list.extend(data_in_list_1)
        # data_in_list = list(set(data_in_list))

        newsarticles_3 = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "country":country,
                }
        })
        response_3 = requests.request("POST", url=self.find, headers=self.header, data=newsarticles_3)
        data_in_list_3 = response_3.json()["documents"]
        data_in_list_3.reverse()
        for i in data_in_list_3:
            if i not in data_in_list:
                data_in_list.append(i)
        # data_in_list.extend(data_in_list_1)
        # data_in_list = list(set(data_in_list))
        # data_in_list.reverse()
        for x in data_in_list:
           try:
            val = self.get_first_image(str=x['news'])
            x['tbnail'] = val["bytes"]
            x['tbfilename'] = None
            x['time_ago'] = self.calculateHour(postdate=x['date'], posttime=x['time'])
            if 'total_words' not in x.keys():
                x["total_words"] = self.get_total_words(x["news"])
           except:
               pass
        if len(data_in_list) < 11:
            return self.get_all_news_content()
        return data_in_list

    def all_news_articles_than_one(self, heading_url):
        news__ = self.view_news_article(heading_url)
        country = news__["country"]
        state = news__["state"]
        category = news__["category"]
        news___ = self.news_get(country=country, state=state, category=category, city=None)
        for i in news___:
            if i["heading_url"] == heading_url:
                del news___[news___.index(i)]
                break
        return news___

    # GET USER'S NEWS

    def get_users_articles(self, user_id):
        newsarticles = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "author_id":user_id,
                "published":True
                }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=newsarticles)
        articles = response.json()["documents"]
        return articles

    # GET BLOG

    def blog_get(self, for_=''):
        blogarticles = json.dumps({
            "collection": "blogarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "published":True
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=blogarticles)
        data_in_list = response.json()["documents"]
        data_in_list.reverse()
        # data_in_list = data_in_list[0:4]
        if for_ == "recent":
            data_in_list = data_in_list[0:10]
        for x in data_in_list:
            val = self.get_first_image(str=x['blog'])
            x['tbnail'] = val["bytes"]
            try:
             x['tbfilename'] = val["filename"][1:]
            except:
                pass
            x['time_ago'] = self.calculateHour(postdate=x['date'], posttime=x['time'])

        return data_in_list

    def all_blog_aritcles_than_one(self, heading_url):
        blogs___ = self.blog_get()
        for i in blogs___:
            if i["heading_url"] == heading_url:
                del blogs___[blogs___.index(i)]
                break

        # blogs___.reverse()
        return blogs___

    # GET USER'S (BLOG)

    def get_users_blog_article(self, user_id):
        blogarticles = json.dumps({
            "collection": "blogarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "author_id":user_id,
                "published":True
                }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=blogarticles)
        articles = response.json()["documents"]
        return articles

    # VIEW (NEWS)

    def view_news_article(self, url_heading):
        newsarticles = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "heading_url":url_heading
                }
        })
        response = requests.request("POST", url=self.findone, headers=self.header, data=newsarticles)
        news = response.json()["document"]
        if news == None:
            return "blog"
        news['time_ago'] = self.calculateHour(postdate=news['date'], posttime=news['time'])
        # news["image"] = self.get_first_image(str=news["news"])
        return news

    # VIEW (BLOG)

    def view_blogs_article(self, url_heading):
        blogarticles = json.dumps({
            "collection": "blogarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "heading_url":url_heading,
                }
        })
        response = requests.request("POST", url=self.findone, headers=self.header, data=blogarticles)
        blog = response.json()["document"]
        blog['time_ago'] = self.calculateHour(postdate=blog['date'], posttime=blog['time'])
        blog['image'] = self.get_first_image(str=blog["blog"])
        return blog

    # DELETION

    # NEWS DEL
    def delete_user_article(self, url_heading, user_id):
        newsarticles = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "heading_url":url_heading,
                }
        })
        response = requests.request("POST", url=self.deleteone, headers=self.header, data=newsarticles)
        if response.json()["deletedCount"] == 0:
            self.delete_blog_user_article(url_heading, user_id)
        self.setNotification(user_id=user_id, notify_msg="You have deleted your article successfully")
        return True

    # BLOG DEL
    def delete_blog_user_article(self, url_heading, user_id):
        blogarticles = json.dumps({
            "collection": "blogarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "heading_url":url_heading,
                }
        })
        response = requests.request("POST", url=self.deleteone, headers=self.header, data=blogarticles)
        self.setNotification(user_id=user_id, notify_msg="You have deleted your article successfully")
        return True

    # TODAY WORD
    # def insert_todays_word(self, user_id, word, meaning):
    #     todaysword = json.dumps({
    #         "collection": "todaysword",
    #         "database": "newsmain",
    #         "dataSource": "Cluster0",
    #         "filter":{
    #             "id":"word-today"
    #         },
    #         "update":{
    #             "$set":{"user_id":user_id,
    #             "username":self.get_user_instance(user_id)["username"],
    #             "word":word,
    #             "meaning":meaning,
    #             "word_id":codeId().generate_id(),
    #             "date":datetime.datetime.now().strftime("%d-%m-%Y")
    #             }
    #         }
    #     })
    #     response = requests.request("POST", url=self.updateone, headers=self.header, data=todaysword)
    #     return True

    # def get_todays_word(self):
    #     todaysword = json.dumps({
    #         "collection": "todaysword",
    #         "database": "newsmain",
    #         "dataSource": "Cluster0",
    #         "filter":{
    #             "id":"word-today"
    #         }
    #     })
    #     response = requests.request("POST", url=self.findone, headers=self.header, data=todaysword)
    #     todays_word = response.json()["document"]
    #     return todays_word

    # def is_woftheday_stack_available(self):
    #     todaysword = json.dumps({
    #         "collection": "todaysword",
    #         "database": "newsmain",
    #         "dataSource": "Cluster0",
    #         "filter":{
    #             "id":"word-today"
    #         }
    #     })
    #     response = requests.request("POST", url=self.findone, headers=self.header, data=todaysword)
    #     if response.json()["document"]["date"]==datetime.datetime.now().strftime("%d-%m-%Y"):
    #         return False
    #     return True

    # EDITING

    # EDIT NEWS
    def edit_news(         self,
                           heading,
                           prev_heading_url,
                           news,
                           country,
                           category,
                           state,
                           city='',
                           keywords=[],
                           author_id='',
                           perm_une_=''
                           ) -> bool:
        validdata = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "author_id":author_id,
                "heading_url":prev_heading_url
                },

            })
        response = requests.request("POST", url=self.findone, headers=self.header, data=validdata)
        data = response.json()["document"]
        if data == None:
           return "Update not accepted"
        else:
            pass
        newheadingurl = re.sub(r'[@_!#$%^&*()<>?/\|}{~:]', "", heading)
        newheadingurl = newheadingurl.replace(" ", "-")
        if newheadingurl[-1] == '.':
            newheadingurl = newheadingurl[0:-1]
        newheadingurl = GoogleTranslator(source='auto', target='en').translate(newheadingurl)
        replaced_str = re.sub('[/<\/?^>+(>|$)/g]', "", news)
        total_words = len(replaced_str.split(" "))
        news = self.image_processing_and_uploading(article=news)
        newsarticle = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "heading_url":prev_heading_url
            },
            "update":{
                "$set":{
                 "heading":heading,
                 "heading_url":newheadingurl,
                 "news":news,
                 "read_time":str(total_words/200).split('.')[0],
                 "category":category,
                 "country":country,
                 "state":state,
                 "city":city,
                 "keywords":keywords,
                 "can_display_une":perm_une_,
                 "article_length":len(replaced_str),
                 "total_words":total_words
                }
            }
        })

        response = requests.request("POST", url=self.updateone, headers=self.header, data=newsarticle)

        return True

    def edit_news_draft(   self,
                           heading="",
                           news="",
                           news_id="",
                           country="",
                           category="",
                           state="",
                           city='',
                           keywords='',
                           author_id='',
                           perm_une_='',
                           can_share=False,
                           author="",
                           publish=False,
                           val = 1
                           ) -> bool:
        validdata = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "news_id":news_id
                },

            })
        response = requests.request("POST", url=self.findone, headers=self.header, data=validdata)
        data = response.json()["document"]
        if data == None:
            newsdata = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "document":{
                "news_id":news_id,
                "published":False,
                "val":0
                }
            })
            response = requests.request("POST", url=self.insertone, headers=self.header, data=newsdata)
        else:
            pass
        heading_url = None
        total_words = None
        if publish:
            if len(heading) < 1:
                return 421
            elif len(keywords) < 1:
                return 422
            heading_url = re.sub(r'[@_!#$%^&*()<>?/\|}{~:]', "", heading)
            heading_url = heading_url.replace(" ", "-")
            if heading_url[-1] == '.':
                heading_url = heading_url[0:-1]
                heading_url = GoogleTranslator(source='auto', target='en').translate(heading_url)
            if not self.validheadingurls(heading_url):
                heading_url = heading_url + "-"
            replaced_str = re.sub('[/<\/?^>+(>|$)/g]', "", news)
            total_words = len(replaced_str.split(" "))
            news = self.image_processing_and_uploading(news)
        newsarticle = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "news_id":news_id
            },
            "update":{
                "$set":{
                 "heading":heading,
                 "heading_url":heading_url,
                 "news":news,
                 "category":category,
                 "country":country,
                 "state":state,
                 "city":city,
                 "date":datetime.datetime.now().strftime("%d-%m-%Y"),
                 "time":datetime.datetime.now().strftime("%H:%M"),
                 "keywords":keywords.split(','),
                 "can_display_une":perm_une_,
                 "author_id":author_id,
                 "author":author,
                 "total_words":total_words,
                 "published":publish,
                 "val":val
                }
            }
        })

        response = requests.request("POST", url=self.updateone, headers=self.header, data=newsarticle)
        if publish:
          if can_share:

                recents = json.dumps({
                        "collection": "recents",
                        "database": "newsmain",
                        "dataSource": "Cluster0",
                        "document":{
                            "heading_url":heading_url,
                            "id":"data",
                            "type":"news",
                        }
                        })
                response = requests.request("POST", url=self.insertone, headers=self.header, data=recents)
        return 411

    def edit_blog_draft(self,
                           heading="",
                           author_id="",
                           blog_id="",
                           author="",
                           blog="",
                           keywords="",
                           views=0,
                           can_share=False,
                           publish=False,
                           val = 1
                           ) -> bool:
        validdata = json.dumps({
            "collection": "blogarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "blog_id":blog_id
                },
            })
        response = requests.request("POST", url=self.findone, headers=self.header, data=validdata)
        data = response.json()["document"]
        if data == None:
            newsdata = json.dumps({
            "collection": "blogarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "document":{
                "blog_id":blog_id,
                "published":False,
                "val":0
                }
            })
            response = requests.request("POST", url=self.insertone, headers=self.header, data=newsdata)
        else:
            pass
        heading_url = None
        total_words = None
        read_time = None
        replaced_str = ''
        if publish:
            if len(heading) < 1:
                return 421
            elif(len(keywords) < 1):
                return 422
            heading_url = re.sub(r'[@_!#$%^&*()<>?/\|}{~:]', "", heading)
            heading_url = heading_url.replace(" ", "-")
            if heading_url[-1] == '.':
                heading_url = heading_url[0:-1]
            heading_url = GoogleTranslator(source='auto', target='en').translate(heading_url)
            if not self.validheadingurls(heading_url):
                # return "Invalid heading"
                heading_url = heading_url + "-"
            replaced_str = re.sub('[/<\/?^>+(>|$)/g]', "", blog)
            total_words = len(replaced_str.split(" "))
            blog = self.image_processing_and_uploading(blog)
            read_time = str(total_words/200).split('.')[0]
        blogarticle = json.dumps({
            "collection": "blogarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "blog_id":blog_id
            },
            "update" :{
                "$set":{
                 "heading":heading,
                 "heading_url":heading_url,
                 "blog_id":blog_id,
                 "author":author,
                 "date":datetime.datetime.now().strftime("%d-%m-%Y"),
                 "time":datetime.datetime.now().strftime("%H:%M"),
                 "author_id":author_id,
                 "blog":blog,
                 "read_time":read_time,
                 "keywords":keywords.split(","),
                 "views":views,
                 "reports":[],
                 "article_length":len(replaced_str),
                 "total_words":total_words,
                 "published":publish,
                 "val":val
            }
          }
        })

        response = requests.request("POST", url=self.updateone, headers=self.header, data=blogarticle)
        if publish:
         if can_share:
          recents = json.dumps({
            "collection": "recents",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "document":{
                 "heading_url":heading_url,
                 "id":"data",
                 "type":"blog",
            }
            })
          response = requests.request("POST", url=self.insertone, headers=self.header, data=recents)
         self.setNotification(user_id=author_id, notify_msg= f"{heading} - uploaded successfully")
        return 411

    # EDIT BLOG
    def edit_blog(self,
                           heading,
                           prev_heading_url,
                           blog,
                           keywords=[],
                           author_id=''
                           ) -> bool:

        validdata = json.dumps({
            "collection": "blogarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "author_id":author_id,
                "heading_url":prev_heading_url
                },

            })
        response = requests.request("POST", url=self.findone, headers=self.header, data=validdata)
        data = response.json()["document"]
        if data == None:
           return "Update not accepted"
        else:
            pass

        newheadingurl = re.sub(r'[@_!#$%^&*()<>?/\|}{~:]', "", heading)
        newheadingurl = newheadingurl.replace(" ", "-")
        if newheadingurl[-1] == '.':
            newheadingurl = newheadingurl[0:-1]
        newheading_url = GoogleTranslator(source='auto', target='en').translate(newheadingurl)
        replaced_str = re.sub('[/<\/?^>+(>|$)/g]', "", blog)
        total_words = len(replaced_str.split(" "))
        blog = self.image_processing_and_uploading(article=blog)
        blogarticle = json.dumps({
            "collection": "blogarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "heading_url":prev_heading_url
            },
            "update":{
                "$set":{
                 "heading":heading,
                 "heading_url":newheading_url,
                 "blog":blog,
                 "read_time":str(total_words/200).split('.')[0],
                 "description":blog[0:40]+"...",
                 "keywords":keywords,
                 "article_length":len(replaced_str),
                 "total_words":total_words
                }
            }
        })

        response = requests.request("POST", url=self.updateone, headers=self.header, data=blogarticle)

        return True

   # ARTICLE

    def getarticle_instance(self, heading_url, val):
        article = json.dumps({
            "collection": val,
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "heading_url":heading_url
            },
            })
        response = requests.request("POST", url=self.findone, headers=self.header, data=article)
        return response.json()["document"]

    def get_user_by_article(self, heading_url, val):
        article = json.dumps({
            "collection": val,
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "heading_url":heading_url
            }
            })
        response = requests.request("POST", url=self.findone, headers=self.header, data=article)
        return response.json()["document"]["author_id"]

    def get_reports_of_articles(self, heading_url, val):
        report = json.dumps({
            "collection": val,
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "heading_url":heading_url
            }
        })
        response = requests.request("POST", url=self.findone, headers=self.header, data=report)
        return response.json()["document"]["reports"]

    # REPORTING

    # REPORT BLOG
    def report_blog(self, heading_url, reporter_id):
        report = json.dumps({
            "collection": "blogarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "heading_url":heading_url
            },
            "update":{
                "$push":{
                    "reports":reporter_id
                }
            }
            })
        if reporter_id not in self.get_reports_of_articles(heading_url, "blogarticles"):
         response = requests.request("POST", url=self.updateone, headers=self.header, data=report)
         return True
        else:
         return "You already reported this article"

    # REPORT NEWS
    def report_news(self, heading_url, reporter_id):
        report = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "heading_url":heading_url
            },
            "update":{
                "$push":{
                    "reports":reporter_id
                }
            }
            })
        if reporter_id not in self.get_reports_of_articles(heading_url, "newsarticles"):
         response = requests.request("POST", url=self.updateone, headers=self.header, data=report)
         return True
        else:
         return "You already reported this article"

    def get_all_news_content(self):
        articles = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "published":True
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=articles)
        response__ = response.json()["documents"]
        response__.reverse()
        for x in response__:
          try:
            val = self.get_first_image(str=x['news'])
            x['tbnail'] = val["bytes"]
            x['tbfilename'] = val["filename"]
            x['time_ago'] = self.calculateHour(postdate=x['date'], posttime=x['time'])
            if 'total_words' not in x.keys():
                x["total_words"] = self.get_total_words(x["news"])
          except:
              pass
        return response__

    # VERIFICATION

    def send_verification_code(self, email, user_id, username):
        code = codeId().generate_verify_code()
        msg = f"""
            Hi,{username}
            Please enter this code in the required field,
               Email confirmation code : {code}
        """
        val = SendEmail().send_email(msg=msg, to=email, subject="Email | Confirmation | lastevents.space")
        verify_id = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id,
            },
            "update":{
                "$set":{
                    "verify_id":code
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=verify_id)
        return True

    def check_verification_code(self, email, user_id, code):
        org_code = self.get_user_instance(user_id=user_id)["verify_id"]
        if int(code) == org_code:
            verify_id = json.dumps({
                "collection": "users",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "user_id":user_id,
                },
                "update":{
                    "$set":{
                        "verified":1
                    }
                }
            })
            response = requests.request("POST", url=self.updateone, headers=self.header, data=verify_id)
            return True
        else:
            return False

    def is_verified(self, user_id):
        data = self.get_user_instance(user_id=user_id)
        verified = data["verified"]
        if verified == 1:
            return True
        else:
            return False

    # HEADING URLS

    def get_heading_urls(self):
        heading_url__ = json.dumps({
            "collection": "ids",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "id":"data"
                }
            })
        response = requests.request("POST", url=self.findone, headers=self.header, data=heading_url__)
        heading_urls = response.json()["document"]["heading_urls"]
        return heading_urls

    def get_news_by_id(self, news_id, user_id):
            news_ = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "news_id":news_id,
                "author_id":user_id
                }
            })
            response = requests.request("POST", url=self.findone, headers=self.header, data=news_)
            response_ = response.json()["document"]
            return response_

    def get_blog_by_id(self, blog_id, user_id):
            blog_ = json.dumps({
            "collection": "blogarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "blog_id":blog_id,
                "author_id":user_id
                }
            })
            response = requests.request("POST", url=self.findone, headers=self.header, data=blog_)
            response_ = response.json()["document"]
            return response_

    def get_articles_by_heading_url(self, heading_urls):
        articles = []
        for i in heading_urls:
            heading_url__ = json.dumps({
            "collection": "blogarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "heading_url":i
                }
            })
            response = requests.request("POST", url=self.findone, headers=self.header, data=heading_url__)
            response_ = response.json()["document"]
            if response_ == None:
                heading_url__ = json.dumps({
                "collection": "newsarticles",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "heading_url":i
                    }
                })
                response = requests.request("POST", url=self.findone, headers=self.header, data=heading_url__)
                response_ = response.json()["document"]
                articles.append(response_)
            else:
                articles.append(response_)

        return articles

    def get_description(self, html):
        htmlparser = BeautifulSoup(html, 'html.parser')
        _list = htmlparser.find_all()
        value = ''
        for i in _list:
            if str(i)[0:4] != '<img':
                value = str(i)
                break
            else:
                pass
        return value

    # TIME CALUCALATOR

    def calculateHour(self, posttime, postdate):
        now = datetime.datetime.now()
        currenttime = now.strftime("%H:%M")
        currentdate = now.strftime("%d-%m-%Y")
        currenttime = currenttime.split(':')
        currentdate = currentdate.split('-')
        currenthour = int(currenttime[0])
        currentday = int(currentdate[0])
        currentmonth = int(currentdate[1])
        currentyear = int(currentdate[-1])
        currentminute = int(currenttime[1])
        posttime = posttime.split(":")
        postdate = postdate.split("-")
        postday = int(postdate[0])
        postmonth = int(postdate[1])
        postyear = int(postdate[-1])
        posthour = int(posttime[0])
        postminute = int(posttime[1])
        monthWith31days = [1, 3, 5, 7, 8, 10, 12]
        monthWith30days = [4, 6, 9, 11]
        monthWith28or29days = [2]
        val = None
        if currentyear == postyear:
            if currentmonth == postmonth:
                if (currentday - postday) == 1:
                    timehour = datetime.timedelta(hours=currenthour, minutes=currentminute, seconds=0, days=1)
                    timehour1 = datetime.timedelta(hours=posthour, minutes=postminute, seconds=0, days=0)
                    val = timehour  - timehour1
                if (currentday - postday) == 0:
                    timehour = datetime.timedelta(hours=currenthour, minutes=currentminute, seconds=0, days=0)
                    timehour1 = datetime.timedelta(hours=posthour, minutes=postminute, seconds=0, days=0)
                    val = timehour - timehour1
            else:
                if (currentmonth - postmonth) == 1:
                    if postmonth in monthWith31days:
                        if currentday - postday == -30:
                            # val = currenthour - posthour
                            timehour = datetime.timedelta(hours=currenthour, minutes=currentminute, seconds=0, days=1)
                            timehour1 = datetime.timedelta(hours=posthour, minutes=postminute, seconds=0, days=0)
                            val = timehour  - timehour1
                            # if val == 0:
                            #     val = 24 - (currenthour + posthour)

                            # if val < 0:
                            #     val = -(val)
                            try:
                             if int(str(val).split(":")[0]) == 0:
                                val = 24 - (currenthour + posthour)

                             if int(str(val).split(":")[0]) < 0:
                                val = -(val)
                            except:
                              pass

                    elif postmonth in monthWith30days:
                        if currentday - postday == -29:
                            # val = currenthour - posthour
                            # val = (currenthour + posthour) - ((24 - posthour) + (24 - currenthour) - 1)
                            timehour = datetime.timedelta(hours=currenthour, minutes=currentminute, seconds=0, days=0)
                            timehour1 = datetime.timedelta(hours=posthour, minutes=postminute, seconds=0, days=1)
                            val = timehour  - timehour1

                    elif postmonth in monthWith28or29days:
                        if currentday - postday == -28 or currentday - postday == -27:
                            # val = currenthour - posthour
                            timehour = datetime.timedelta(hours=currenthour, minutes=currentminute, seconds=0, days=0)
                            timehour1 = datetime.timedelta(hours=posthour, minutes=postminute, seconds=0, days=1)
                            val = timehour  - timehour1

        if val == None:
            return None
        if len(str(val)) > 8:
            pass
        else:
           time_split = str(val).split(":")
           if time_split[0] == '0':
               return time_split[1] + 'min ago'
           else:
            return time_split[0] + "h ago"

    # NOTIFICATIONS

    def setNotification(self, user_id, notify_msg):
            notify_id = codeId().generate_id()
            notify = json.dumps({
                "collection": "notifications",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "document":{
                    "user_id":user_id,
                    "notify_msg":notify_msg,
                    "date":datetime.datetime.now().strftime("%d-%m-%Y"),
                    "time":datetime.datetime.now().strftime("%H:%M"),
                    "notify_id":notify_id
                    }
                })
            response = requests.request("POST", url=self.insertone, headers=self.header, data=notify)

    def deleteNotifications(self, user_id, notify_id):
            notify = json.dumps({
                "collection": "notifications",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "user_id":user_id,
                    "notify_id":notify_id
                    }
                })
            response = requests.request("POST", url=self.deleteone, headers=self.header, data=notify)

    def getNotifcations(self, user_id):
            notify = json.dumps({
                "collection": "notifications",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "user_id":user_id,
                    }
                })
            response = requests.request("POST", url=self.find, headers=self.header, data=notify)
            notifications = response.json()["documents"]
            for i in notifications:
                i["time_ago"] = self.calculateHour(postdate=i["date"], posttime=i["time"])
            notifications.reverse()
            return notifications

    def deleteAllNotifications(self, user_id):
            notify = json.dumps({
                "collection": "notifications",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "user_id":user_id,
                    }
                })
            response = requests.request("POST", url=self.delete, headers=self.header, data=notify)
            # notifications = response.json()["documents"]

    # COMMENTS

    def setComment(self, user_id, comment_, article_id, author):
            comment_id = codeId().generate_id()
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H:%M")
            comment = json.dumps({
                "collection": "comments",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "document":{
                    "user_id":user_id,
                    "comment":comment_,
                    "author":author,
                    "date":date,
                    "time":time,
                    "comment_id":comment_id,
                    "article_id":article_id
                    }
                })
            response = requests.request("POST", url=self.insertone, headers=self.header, data=comment)
            return {"comment":comment_, "author":author, "date":date}

    def deleteComment(self, user_id, comment_id):
            comment = json.dumps({
                "collection": "comments",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "user_id":user_id,
                    "comment_id":comment_id
                    }
                })
            response = requests.request("POST", url=self.deleteone, headers=self.header, data=comment)

    def getCommentsofArticle(self, article_id):
            comment = json.dumps({
                "collection": "comments",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "article_id":article_id,
                    }
                })
            response = requests.request("POST", url=self.find, headers=self.header, data=comment)
            comments = response.json()["documents"]
            return comments

    def getCommentsofUser(self, user_id):
            comment = json.dumps({
                "collection": "comments",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "user_id":user_id,
                    }
                })
            response = requests.request("POST", url=self.find, headers=self.header, data=comment)
            comments = response.json()["documents"]
            return comments

    def deleteAllComment(self, user_id):
            comment = json.dumps({
                "collection": "comments",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "user_id":user_id,
                    }
                })
            response = requests.request("POST", url=self.delete, headers=self.header, data=comment)

    # DRAFTS

    def createDraft(self, user_id, type_):
            draft_id = codeId().generate_id()
            draft = json.dumps({
                "collection": "drafts",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "document":{
                    "user_id":user_id,
                    "draft_id":draft_id,
                    "heading":'',
                    "article_data":'',
                    "time":datetime.datetime.now().strftime("%H:%M"),
                    "date":datetime.datetime.now().strftime("%d-%m-%Y"),
                    "type":type_
                    }
                })
            response = requests.request("POST", url=self.insertone, headers=self.header, data=draft)
            return draft_id

    def editDraft(self, user_id, draft_id, heading, article_data):
            draft = json.dumps({
                "collection": "drafts",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "user_id":user_id,
                    "draft_id":draft_id,
                    },
                "update":{
                    "$set":{
                        "heading":heading,
                        "article_data":article_data,
                    }
                }
                })
            response = requests.request("POST", url=self.updateone, headers=self.header, data=draft)
            return True

    def is_valid_draft_and_user_id(self, user_id, draft_id):
            draft = json.dumps({
                "collection": "drafts",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "user_id":user_id,
                    "draft_id":draft_id,
                    }
                })
            response = requests.request("POST", url=self.findone, headers=self.header, data=draft)
            data = response.json()["document"]
            if data == None:
                return False
            else:
                return True

    def deletedraft(self, draft_id, user_id):
            draft = json.dumps({
                "collection": "newsarticles",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "author_id":user_id,
                    "news_id":draft_id,
                    }
                })
            response = requests.request("POST", url=self.deleteone, headers=self.header, data=draft)

            return True

    def deletedraftblog(self, draft_id, user_id):
            draft = json.dumps({
                "collection": "blogarticles",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "author_id":user_id,
                    "blog_id":draft_id,
                    }
                })
            response = requests.request("POST", url=self.deleteone, headers=self.header, data=draft)

            return True

    def getdraftsofUser(self, user_id):
            draft = json.dumps({
                "collection": "newsarticles",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "author_id":user_id,
                    "published":False
                },
            })
            response = requests.request("POST", url=self.find, headers=self.header, data=draft)
            drafts = response.json()["documents"]
            if drafts == None:
                pass
            else:
                # for i in drafts:
                    # i["time_ago"] = self.calculateHour(postdate=i["date"], posttime=i["time"])
                # drafts.reverse()
                return drafts

    def getdraftsofUserBlog(self, user_id):
            draft = json.dumps({
                "collection": "blogarticles",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "author_id":user_id,
                    "published":False
                },
            })
            response = requests.request("POST", url=self.find, headers=self.header, data=draft)
            drafts = response.json()["documents"]
            if drafts == None:
                pass
            else:
                # for i in drafts:
                    # i["time_ago"] = self.calculateHour(postdate=i["date"], posttime=i["time"])
                # drafts.reverse()
                return drafts

    def getdraft(self, draft_id):
            draft = json.dumps({
                "collection": "drafts",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "draft_id":draft_id
                },
            })
            response = requests.request("POST", url=self.findone, headers=self.header, data=draft)
            draft_ = response.json()["document"]
            return draft_



    def get_news_and_blog_articles(self):
        li1 = self.get_all_news_content()
        li2 = self.blog_get()
        li1.extend(li2)
        return li1

    # CHAT

    # def insertChat(self, chat_room_id, text, user_id, username):
    #         chat_id = codeId().generate_chat_id()
    #         chat = json.dumps({
    #             "collection": "chats",
    #             "database": "newsmain",
    #             "dataSource": "Cluster0",
    #             "document":{
    #                 "chat_room_id":chat_room_id,
    #                 "text":text,
    #                 "chat_id":chat_id,
    #                 "date":datetime.datetime.now().strftime("%d-%m-%Y"),
    #                 "time":datetime.datetime.now().strftime("%H:%M"),
    #                 "user_id":user_id,
    #                 "username":username
    #             },
    #         })
    #         response = requests.request("POST", url=self.insertone, headers=self.header, data=chat)
    #         return chat_id

    # def getChatsByRoomId(self, chat_room_id):
    #         chat = json.dumps({
    #             "collection": "chats",
    #             "database": "newsmain",
    #             "dataSource": "Cluster0",
    #             "filter":{
    #                 "chat_room_id":chat_room_id
    #             }
    #         })
    #         response = requests.request("POST", url=self.find, headers=self.header, data=chat)
    #         result = response.json()["documents"]
    #         return result

    # def delete_chat(self, chat_id, user_id):
    #         chat = json.dumps({
    #             "collection": "chats",
    #             "database": "newsmain",
    #             "dataSource": "Cluster0",
    #             "filter":{
    #                 "chat_id":chat_id,
    #                 "user_id":user_id
    #             }
    #         })
    #         response = requests.request("POST", url=self.deleteone, headers=self.header, data=chat)
    #         result = response.json()["deletedCount"]
    #         if result != 1:
    #             return "Unauthorized"
    #         return True

    def get_total_words(self, txt):
        replaced_str = re.sub('[/<\/?^>+(>|$)/g]', "", txt)
        total_words = len(replaced_str.split(" "))
        return total_words

    def get_all_users_by_state(self, country, state):
        members = json.dumps({
                "collection": "users",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "state":CountriesStatesCities().getStatesByCountry_(country)[int(state.split('-')[-1][2:])-1]
                }
            })
        response = requests.request("POST", url=self.find, headers=self.header, data=members)
        result = response.json()["documents"]
        return result

    # GROUPS

    # def get_available_countries(self):
    #     members = json.dumps({
    #             "collection": "users",
    #             "database": "newsmain",
    #             "dataSource": "Cluster0"
    #         })
    #     response = requests.request("POST", url=self.find, headers=self.header, data=members)
    #     result = response.json()["documents"]
    #     result_ = list(set([x["country"] for x in result]))
    #     result_.sort()
    #     response = []
    #     for i in result_:
    #         response.append({
    #             "username":f"GROUP-00{CountriesStatesCities().getCountries().index(i) + 1}",
    #             "country":i,
    #             "contributions":self.get_total_contributions_of_country(i)
    #         })
    #     return response

    # def get_available_states(self, country):
    #     members = json.dumps({
    #             "collection": "users",
    #             "database": "newsmain",
    #             "dataSource": "Cluster0",
    #             "filter":{
    #                 "country":CountriesStatesCities().getCountries()[int(country[8:])-1]
    #             }
    #         })
    #     response = requests.request("POST", url=self.find, headers=self.header, data=members)
    #     result = response.json()["documents"]
    #     result_ = list(set([x["state"] for x in result]))
    #     result_.sort()
    #     response = []
    #     for i in result_:
    #         response.append({
    #             "username":f"{country}-S-00{CountriesStatesCities().getStatesByCountry_(country).index(i)+1}",
    #             "state":i,
    #             "contributions":self.get_total_contributions_of_state(country=country, state=i)
    #         })
    #     return response

    # def get_high_contributor_by_country(self, country):
    #     members = json.dumps({
    #             "collection": "users",
    #             "database": "newsmain",
    #             "dataSource": "Cluster0",
    #             "filter":{
    #                 "country":CountriesStatesCities().getCountries()[int(country[8:])-1]
    #             }
    #         })
    #     response = requests.request("POST", url=self.find, headers=self.header, data=members)
    #     result = response.json()["documents"]
    #     high_contributions = result[0]["contributions"]
    #     high_contributor = result[0]
    #     for i in result:
    #         if i["contributions"] > high_contributions:
    #             high_contributions = i["contributions"]
    #             high_contributor = i
    #     return high_contributor

    # def get_high_contributor_by_state(self, country, state):
    #     members = json.dumps({
    #             "collection": "users",
    #             "database": "newsmain",
    #             "dataSource": "Cluster0",
    #             "filter":{
    #                 "country":CountriesStatesCities().getCountries()[int(country[8:])-1],
    #                 "state":CountriesStatesCities().getStatesByCountry_(country)[int(state.split('-')[-1][2:])-1]
    #             }
    #         })
    #     response = requests.request("POST", url=self.find, headers=self.header, data=members)
    #     result = response.json()["documents"]
    #     high_contributions = result[0]["contributions"]
    #     high_contributor = result[0]
    #     for i in result:
    #         if i["contributions"] > high_contributions:
    #             high_contributions = i["contributions"]
    #             high_contributor = i
    #     return high_contributor

    # def get_group_name(self, country):
    #     countries = CountriesStatesCities().getCountries()
    #     index = countries.index(country) + 1
    #     return f"GROUP-00{index}"

    # def get_total_contributions_of_country(self, country):
    #     members = json.dumps({
    #             "collection": "users",
    #             "database": "newsmain",
    #             "dataSource": "Cluster0",
    #             "filter":{
    #                 "country":country,
    #             }
    #         })
    #     response = requests.request("POST", url=self.find, headers=self.header, data=members)
    #     result = response.json()["documents"]
    #     return sum([x["contributions"] for x in result])

    # def is_available_state(self, country):
    #     members = json.dumps({
    #             "collection": "users",
    #             "database": "newsmain",
    #             "dataSource": "Cluster0",
    #             "filter":{
    #                 "country":country
    #             }
    #         })
    #     response = requests.request("POST", url=self.find, headers=self.header, data=members)
    #     result = response.json()["documents"]
    #     result_ = list(set([x["state"] for x in result]))
    #     result_.sort()
    #     return result_

    # def get_total_contributions_of_state(self, country, state):
    #     members = json.dumps({
    #             "collection": "users",
    #             "database": "newsmain",
    #             "dataSource": "Cluster0",
    #             "filter":{
    #                 "country":CountriesStatesCities().getCountries()[int(country[8:])-1],
    #                 "state":state
    #             }
    #         })
    #     response = requests.request("POST", url=self.find, headers=self.header, data=members)
    #     result = response.json()["documents"]
    #     return sum([x["contributions"] for x in result])

    def get_users(self):
        users = json.dumps({
                "collection": "users",
                "database": "newsmain",
                "dataSource": "Cluster0",
            })
        response = requests.request("POST", url=self.find, headers=self.header, data=users)
        return response.json()["documents"]

    # def update_user_incomes(self, user_id, income_this_week, total_earning, balance):
    #     updateuser = json.dumps({
    #         "collection": "users",
    #         "database": "newsmain",
    #         "dataSource": "Cluster0",
    #         "filter":{
    #             "user_id":user_id
    #         },
    #         "update":{
    #             "$set":{
    #                 "last_month_earning":0,
    #                 "total_earning":0,
    #                 "balance":0,
    #             }
    #         }
    #     })
    #     response = requests.request("POST", url=self.updateone, headers=self.header, data=updateuser)

    # PAYMENTS

    def update_user_incomes(self, user_id, income_this_week, total_earning, balance):
        updateuser = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
            },
            "update":{
                "$set":{
                    "last_month_earning":income_this_week,
                    "total_earning":round(total_earning+income_this_week, 2),
                    "balance":round(balance+income_this_week, 2),
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=updateuser)

    def insert_payment_time(self, week_no, week_val):
        payment = json.dumps({
            "collection": "payment_time",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "document":{
                "week_no":week_no,
                "week_val":week_val,
                "date":datetime.datetime.now().strftime("%d-%m-%Y"),
                "time":datetime.datetime.now().strftime("%H:%M")
            }
        })
        response = requests.request("POST", url=self.insertone, headers=self.header, data=payment)
        return True

    def last_payment_document(self):
        payment = json.dumps({
            "collection": "payment_time",
            "database": "newsmain",
            "dataSource": "Cluster0",
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=payment)
        return response.json()["documents"][-1]

    # IMAGES PROCESSING

    def image_processing_and_uploading(self, article):
      soup = BeautifulSoup(article, 'html.parser')
      imgs = soup.find_all("img")
      news = article
      if len(imgs) > 0:
        for i in imgs:
            image = str(i).split("src=")[1].split()[0][1:-1]
            # f = urllib.request.urlopen(image).fp
            # f = io.BytesIO(fobj)
            filename = codeId().generate_image_filename()
            if image[0:4] == "data":
                with open(f"/home/forlanching/mysite/NewFolder/images/{filename}", "wb") as file:
                    dec = base64.b64decode(image.split(",")[1].encode())
                    file.write(dec)
                AwsS3().upload_in_s3(filename=f"/home/forlanching/mysite/NewFolder/images/{filename}", objname=filename)
                news = news.replace(image, f"/images/im342/{filename}")
                os.remove(f"/home/forlanching/mysite/NewFolder/images/{filename}")
            else:
                pass
            # AwsS3().upload_in_s3(fileobj=dec, objname=filename)
            # news = news.replace(image, f"http://images.lastevents.space/{filename}")
        return news
      else:
          return news

    def image_processing_and_uploading_fomr(self, img):
            # f = urllib.request.urlopen(image).fp
            # f = io.BytesIO(fobj)
            filename = codeId().generate_image_filename()
            fileextension = img.filename.split(".")[-1]
            img.filename = filename
            img.filename = img.filename.replace(".jpg", "."+fileextension)
            img.save(os.path.join("/home/forlanching/mysite/NewFolder/images", img.filename))
            # img.save("/home/forlanching/mysite/NewFolder/images/{img.filename}")
            # AwsS3().upload_in_s3(filename=f"/home/forlanching/mysite/NewFolder/images/{img.filename}", objname=img.filename)
            AwsS3().upload_in_s3(filename=os.path.join("/home/forlanching/mysite/NewFolder/images", img.filename), objname=img.filename)
            os.remove(os.path.join("/home/forlanching/mysite/NewFolder/images", img.filename))
            # os.remove(f"/home/forlanching/mysite/NewFolder/images/{img.filename}")
            return f"/images/im342/{img.filename}"
            # AwsS3().upload_in_s3(fileobj=dec, objname=filename)
            # news = news.replace(image, f"http://images.lastevents.space/{filename}")

    def get_first_image(self, str):
        if "<img " in str:
         try:
            # _ = str.split("<")
            # c = [x for x in _ if "src" in x]
            # d = c[0].split("src=")[-1][1:].split("style")[0][1:-2]
            # filename = c[0].split('data-filename')[-1].split('=')[-1][0:-2]
            _ = str.split("<")
            c = [x for x in _ if "src" in x]
            d = c[0].split("src=")[-1][1:].split(" ")
            bytes = d[0][:-1]
            filename = d[-1].split("=")[-1][1:-2]
            return {"bytes":bytes, "filename":filename}
         except:
            return{"bytes":None, "filename":None}
        return{"bytes":None, "filename":None}

    # UPDATE (PAYMENTS)

    def updatephonenumber(self, user_id, phoneno, cc):
        user_instance = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
            },
            "update":{
                "$set":{
                    "phoneno":phoneno,
                    "cc":cc
                }
           }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=user_instance)
        return True

    def updateaccountnumber(self, user_id, accno, ifsc):
        user_instance = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
            },
            "update":{
                "$set":{
                        "accno":accno,
                        "ifsc":ifsc,
                        "date":datetime.datetime.now().strftime("%d-%m-%Y")
                    }
                }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=user_instance)
        return True

    # TRANSACTIONS

    def send_transact(self, user_id, amount):
        user_instance = self.get_user_instance(user_id=user_id)
        if "accno" not in user_instance.keys():
            user_instance["accno"] = ""
            user_instance["ifsc"] = ""
        if "phoneno" not in user_instance.keys():
            user_instance["phoneno"] = ""
            user_instance["cc"] = ""
        msg = f"""
            USERNAME : {user_instance["username"]}
            Account Number : {user_instance["accno"]}
            IFSC : {user_instance["ifsc"]}
            PHONE NUMBER : {user_instance["phoneno"]}
            COUNTRY CODE : {user_instance["cc"]}
            AMOUNT : {amount}
            BEFORE BALANCE : {user_instance["balance"]}
        """
        SendEmail().send_email(msg=msg, to="help@lastevents.space", subject="Transaction | LASTEVENTS.SPACE")

    def save_transact(self, user_id, amount, username):
        transact_id = codeId().generate_id() + "t"
        user_instance = json.dumps({
            "collection": "transactions",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "document":{
                 "date":datetime.datetime.now().strftime("%d-%m-%Y"),
                 "time":datetime.datetime.now().strftime("%H:%M"),
                "amount":amount,
                "user_id":user_id,
                "username":username,
                "status":"not yet",
                "transact_id":transact_id
            }
            })
        response = requests.request("POST", url=self.insertone, headers=self.header, data=user_instance)

    def update_balance(self, user_id, newbalance):
        updateuser = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
            },
            "update":{
                "$set":{
                    "balance":newbalance
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=updateuser)

    def update_transaction_status(self, transact_id, status):
        updatetransaction = json.dumps({
            "collection": "transactions",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "transact_id":transact_id
            },
            "update":{
                "$set":{
                    "status":status
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=updatetransaction)
        return True

    def deleteaccno(self, user_id):
        updateuser = json.dumps({
            "collection": "users",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
            },
            "update":{
                "$set":{
                    "accno":"",
                    "ifsc":""
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=updateuser)

    # MEMES & OPINIONS

    def create_opinion_post(self, user_id, username, keywords, text, image):
        post_id = codeId().generate_post_id()
        pagename = self.get_page_name_by_user_id(user_id)
        if pagename == False:
            return "Not able to create"
        opinion = json.dumps({
            "collection": "opinions",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "document":{
                "image":image,
                "keywords":keywords,
                "text":text,
                "username":username,
                "user_id":user_id,
                "pagename":pagename,
                "post_id":post_id,
                "date":datetime.datetime.now().strftime("%d-%m-%Y"),
                "time":datetime.datetime.now().strftime("%H:%M"),
                "valuable":0,
                "comments":0,
                "shares":0,
                "views":0,
            }
        })
        response = requests.request("POST", url=self.insertone, headers=self.header, data=opinion)
        return post_id

    def delete_opinion_post(self, user_id, post_id):
        opinion = json.dumps({
            "collection": "opinions",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id,
                "post_id":post_id
            }
        })
        response = requests.request("POST", url=self.deleteone, headers=self.header, data=opinion)
        if response.json()["deletedCount"] == 0:
            return "Not valid"
        return response.text

    def get_opinion_post(self, user_id, post_id):
        opinion = json.dumps({
            "collection": "opinions",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id,
                "post_id":post_id
            }
        })
        response = requests.request("POST", url=self.findone, headers=self.header, data=opinion)
        value = response.json()["document"]
        if response.json()["document"] == None:
            return "Not valid"
        return value

    def edit_opinion_post(self, user_id, post_id, text):
        opinion = json.dumps({
            "collection": "opinions",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id,
                "post_id":post_id
            },
            "update":{
                "$set":{
                    "text":text
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=opinion)
        # value = response.json()["document"]
        if response.json()["modifiedCount"] == 0:
            return "Not valid"
        return response.text

    def update_opinion_value(self, post_id):
        opinion = json.dumps({
            "collection": "opinions",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "post_id":post_id
            },
            "update":{
                "$set":{
                    "valuable":len(self.get_all_opinion_values(post_id))
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=opinion)
        # value = response.json()["document"]
        if response.json()["modifiedCount"] == 0:
            return "Not valid"
        return response.text

    def update_opinion_comment(self, post_id):
        opinion = json.dumps({
            "collection": "opinions",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "post_id":post_id
            },
            "update":{
                "$set":{
                    "comments":len(self.get_all_opinion_comments(post_id))
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=opinion)
        # value = response.json()["document"]
        if response.json()["modifiedCount"] == 0:
            return "Not valid"
        return response.text

    def insert_opinion_value(self, user_id, post_id):
        opinion = json.dumps({
            "collection": "opinionvalues",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "document":{
               "user_id":user_id,
               "post_id":post_id,
            }
        })
        if self.is_valid_opinion_value(user_id, post_id):
            response = requests.request("POST", url=self.insertone, headers=self.header, data=opinion)
            self.update_opinion_value(post_id=post_id)
            return True
        else:
            if self.delete_opinion_value(user_id, post_id):
             self.update_opinion_value(post_id=post_id)
             return False
            else:
                pass

    def is_valid_opinion_value(self, user_id, post_id):
        opinion = json.dumps({
            "collection": "opinionvalues",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
               "user_id":user_id,
               "post_id":post_id,
            }
        })
        response = requests.request("POST", url=self.findone, headers=self.header, data=opinion)
        if response.json()["document"] == None:
            return True
        else:
            return False

    def delete_opinion_value(self, user_id, post_id):
        opinion = json.dumps({
            "collection": "opinionvalues",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
               "user_id":user_id,
               "post_id":post_id,
            }
        })
        response = requests.request("POST", url=self.deleteone, headers=self.header, data=opinion)
        if response.json()["deletedCount"] == 1:
            return True
        else:
            return False

    def get_all_opinion_values(self, post_id):
        opinion = json.dumps({
            "collection": "opinionvalues",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
               "post_id":post_id,
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=opinion)
        value = response.json()["documents"]
        return value

    def get_all_opinion_comments(self, post_id):
        opinion = json.dumps({
            "collection": "comments",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
               "article_id":post_id,
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=opinion)
        value = response.json()["documents"]
        return value

    def get_opinions_of_user(self ,user_id):
        opinion = json.dumps({
            "collection": "opinions",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
               "user_id":user_id,
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=opinion)
        value = response.json()["documents"]
        return value

    # PAGES

    def createPage(self, pagename, pagedescription, pagepurpose, username, user_id):
        page_id = codeId().generate_page_id()
        opinion = json.dumps({
            "collection": "page",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "document":{
                "pageid":page_id,
               "pagename":pagename,
               "pagedescription":pagedescription,
               "pagepurpose":pagepurpose,
               "date":datetime.datetime.now().strftime("%d-%m-%Y"),
               "time":datetime.datetime.now().strftime("%H:%M"),
               "created_by":username,
               "user_id":user_id,
               "pagevisits":0,
               "totalviews":0,
               "totalvalue":0
            }
        })
        response = requests.request("POST", url=self.insertone, headers=self.header, data=opinion)
        # value = response.json()["document"]
        return page_id

    def is_valid_pagename(self, pagename):
        opinion = json.dumps({
            "collection": "page",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                 "pagename":pagename
            }
        })
        response = requests.request("POST", url=self.findone, headers=self.header, data=opinion)
        if response.json()["document"] != None:
           return False
        return True

    def deletePage(self, pagename, user_id):
        opinion = json.dumps({
            "collection": "page",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                 "pagename":pagename,
                 "user_id":user_id
            }
        })
        response = requests.request("POST", url=self.deleteone, headers=self.header, data=opinion)
        if response.json()["deletedCount"] == 0:
           return "Invalid request"
        self.deletepageposts(pagename=pagename)
        return True

    def deletepageposts(self, pagename):
        opinion = json.dumps({
            "collection": "opinions",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                 "pagename":pagename,
            }
        })
        response = requests.request("POST", url=self.delete, headers=self.header, data=opinion)

    def getPage(self, user_id):
        opinion = json.dumps({
            "collection": "page",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                 "user_id":user_id
            }
        })
        response = requests.request("POST", url=self.findone, headers=self.header, data=opinion)
        value = response.json()["document"]
        if value == None:
           return "No Page Found"
        return value

    def get_all_opis(self):
        opinion = json.dumps({
            "collection": "opinions",
            "database": "newsmain",
            "dataSource": "Cluster0"
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=opinion)
        value = response.json()["documents"]
        return value

    def get_page_name_by_user_id(self, user_id):
        pagename = json.dumps({
            "collection": "page",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
            }
        })
        response = requests.request("POST", url=self.findone, headers=self.header, data=pagename)
        value = response.json()["document"]
        if value == None:
            return False
        return value["pagename"]

    def get_pageview(self, pagename):
        pagename = json.dumps({
            "collection": "page",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "pagename":pagename
            }
        })
        response = requests.request("POST", url=self.findone, headers=self.header, data=pagename)
        value = response.json()["document"]
        if value == None:
            return False
        return value

    def get_pageposts(self, pagename):
        pagename = json.dumps({
            "collection": "opinions",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "pagename":pagename
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=pagename)
        value = response.json()["documents"]
        if value == None:
            return False
        return value

    def get_all_pages(self):
        opinion = json.dumps({
            "collection": "page",
            "database": "newsmain",
            "dataSource": "Cluster0",
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=opinion)
        value = response.json()["documents"]
        return value

    # OPI STATS

    def count_total_opi_of_user(self, user_id):
        usposts = json.dumps({
            "collection": "opinions",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "user_id":user_id
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=usposts)
        value = response.json()["documents"]
        return value

    def count_total_opi_by_pagename(self, pagename):
        usposts = json.dumps({
            "collection": "opinions",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "pagename":pagename
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=usposts)
        value = response.json()["documents"]
        return value

    def get_page_total_posts(self):
        pages = BackEnd().get_all_pages()
        for i in pages:
            posts = BackEnd().count_total_opi_by_pagename(pagename=i["pagename"])
            i["total_posts"] = len(posts)
        return pages

    def get_page_total_value(self, pages):
        total_value = 0
        for i in pages:
            posts = BackEnd().count_total_opi_by_pagename(pagename=i["pagename"])
            for j in posts:
                total_value += j["valuable"]
            i["totalvalue"] = total_value
            total_value = 0

        return pages

    def get_page_total_value_(self, page):
        total_value = 0
        posts = BackEnd().count_total_opi_by_pagename(pagename=page["pagename"])
        for j in posts:
            total_value += j["valuable"]

        return total_value

    def get_news_from_exact(self, country, state, category, city):
        news_ = {
            "fromcity":[],
            "fromstate":[],
            "fromcountry":[],
            "fromcategory":[],
            "fromexact":[]
        }

        newsarticles = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "country":country,
                "state":state,
                "category":category,
                "city":city
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=newsarticles)
        data_in_list = response.json()["documents"]
        data_in_list.reverse()
        news_["fromexact"] = data_in_list

        newsarticles_1 = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "country":country,
                "state":state,
                "category":category
            }
        })
        response_1 = requests.request("POST", url=self.find, headers=self.header, data=newsarticles_1)
        data_in_list_1 = response_1.json()["documents"]
        data_in_list_1.reverse()
        for i in data_in_list_1:
            if i not in data_in_list:
                news_["fromcategory"].append(i)
        # data_in_list.extend(data_in_list_1)
        # data_in_list = list(set(data_in_list))

        newsarticles_2 = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "country":country,
                "state":state,            }
        })
        response_2 = requests.request("POST", url=self.find, headers=self.header, data=newsarticles_2)
        data_in_list_2 = response_2.json()["documents"]
        data_in_list_2.reverse()
        for i in data_in_list_2:
            if i not in data_in_list:
                news_["fromstate"].append(i)
        # data_in_list.extend(data_in_list_1)
        # data_in_list = list(set(data_in_list))

        newsarticles_3 = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "country":country,
                }
        })
        response_3 = requests.request("POST", url=self.find, headers=self.header, data=newsarticles_3)
        data_in_list_3 = response_3.json()["documents"]
        data_in_list_3.reverse()
        for i in data_in_list_3:
            if i not in data_in_list:
                news_["fromcountry"].append(i)
        # data_in_list.extend(data_in_list_1)
        # data_in_list = list(set(data_in_list))
        # data_in_list.reverse()
        for x in data_in_list:
            val = self.get_first_image(str=x['news'])
            x['tbnail'] = val["bytes"]
            x['tbfilename'] = None
            x['time_ago'] = self.calculateHour(postdate=x['date'], posttime=x['time'])
            if 'total_words' not in x.keys():
                x["total_words"] = self.get_total_words(x["news"])

        if len(data_in_list) < 11:
            return self.get_all_news_content()
        return data_in_list

    def get_city(self, country, state, city):
        newsarticles = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "country":country,
                "state":state,
                "city":city,
                "published":True
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=newsarticles)
        data_in_list = response.json()["documents"]
        data_in_list.reverse()
        return data_in_list

    def get_state(self, country, state):
        newsarticles = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "country":country,
                "state":state,
                "published":True
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=newsarticles)
        data_in_list = response.json()["documents"]
        data_in_list.reverse()
        return data_in_list

    def get_country(self, country):
        newsarticles = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "country":country,
                "published":True
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=newsarticles)
        data_in_list = response.json()["documents"]
        data_in_list.reverse()
        return data_in_list

    def get_category(self, country, category):
        newsarticles = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "country":country,
                "category":category
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=newsarticles)
        data_in_list = response.json()["documents"]
        data_in_list.reverse()
        return data_in_list

    def get_exact(self, country, category, state, city):
        newsarticles = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "country":country,
                "category":category,
                "state":state,
                "city": city,
                "published":True
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=newsarticles)
        data_in_list = response.json()["documents"]
        data_in_list.reverse()
        return data_in_list

    def update_page_description(self, pagename, pagedescription, user_id):
        if len(pagedescription) > 100   :
            return 211
        page = json.dumps({
            "collection": "page",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                 "pagename":pagename,
                 "user_id":user_id
            },
            "update":{
                "$set":{
                    "pagedescription":pagedescription
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=page)
        resp = response.json()
        if resp["matchedCount"] == 1:
           return True
        else:
            return False


    def action_1(self):
        news = json.dumps({
                "collection": "newsarticles",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "country":""
                    }
                })
        response = requests.request("POST", url=self.delete, headers=self.header, data=news)

    def action_2(self):
        news = json.dumps({
                "collection": "newsarticles",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                },
                "update":{
                    "$set":{
                      "published":True
                    }
                }
                })
        response = requests.request("POST", url=self.update, headers=self.header, data=news)

    def action_3(self):
        blog = json.dumps({
                "collection": "blogarticles",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                },
                "update":{
                    "$set":{
                      "published":True
                    }
                }
                })
        response = requests.request("POST", url=self.update, headers=self.header, data=blog)

    def deleteaccount(self, user_id):
        user = json.dumps({
                "collection": "users",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                  "user_id":user_id
                },

                })
        response = requests.request("POST", url=self.deleteone, headers=self.header, data=user)

# for i in range(10):
#  BackEnd().setNotification(user_id="XmiID08230071792", notify_msg="message testing")
#    BackEnd().create_opinion_post(user_id="XmiID08230071792", username="soory", text="helloworld", keywords=[], image="http://images.lastevents.space/noload.jpg")
# BackEnd().action_3()
# BackEnd().action_2()
