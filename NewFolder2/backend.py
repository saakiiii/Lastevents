import json
import re
from colorama import Back
from flask import jsonify
import requests
from codegenerator import codeId
import datetime
import bcrypt
from EmailApi import SendEmail
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

class BackEnd:

    def __init__(self) -> None:
        self.findone = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/findOne"
        self.updateone = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/updateOne"
        self.insertone = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/insertOne"
        self.deleteone = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/deleteOne"
        self.find = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/find"
        self.delete = "https://data.mongodb-api.com/app/data-ytrxs/endpoint/data/v1/action/deleteMany"
        self.header = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': "UOGuFyCP3TfwSzHGQo1aOOU5Q5OQK7xPK3xlLsY6T2EWo8WKYxzD7AagtMYAtpY2",
        }

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
        newdataids = json.dumps({
            "collection": "ids",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "id":"data"
            },
            "update":{
                "$push":{
                    "emails":email,
                    "usernames":username
                }
            }
            })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=newdataids)
        self.setNotification(user_id=user_id, notify_msg="Welcome to lastevents.space, enter into the space")
        return {"user_id":user_id, "password":password}

    def validemail(self, email):
        email_ = json.dumps({
            "collection": "ids",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "id":"data"
                }
            })
        response = requests.request("POST", url=self.findone, headers=self.header, data=email_)
        emails = response.json()["document"]["emails"]
        if email in emails:
            return False
        else:
            return True

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
            "collection": "ids",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "id":"data"
                }
            })
        response = requests.request("POST", url=self.findone, headers=self.header, data=username_)
        usernames = response.json()["document"]["usernames"]
        if username in usernames:
            return False
        else:
            return True

    def validheadingurls(self, heading_url):
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
        if heading_url in heading_urls:
            return False
        else:
            return True

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
        increment = self.increment_article_counts(data)

        newdataids = json.dumps({
            "collection": "ids",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "id":"data"
            },
            "update":{
                "$push":{
                 "heading_urls":heading_url
                }
            }
            })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=newdataids)
        self.setNotification(user_id=author_id, notify_msg= "Your last news post has been uploaded successfully")
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
        data = self.get_user_instance(user_id=author_id)
        increment = self.increment_article_blog_counts(data)

        newdataids = json.dumps({
            "collection": "ids",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "id":"data"
            },
            "update":{
                "$push":{
                 "heading_urls":heading_url
                }
            }
            })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=newdataids)
        self.setNotification(user_id=author_id, notify_msg= "Your last blog post has been uploaded successfully")
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

    def increment_article_counts(self, data):
        contributions = data["contributions"]
        today_total_articles = data["today_total_articles"]
        total_articles = data["total_articles"]
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
                    "contributions":contributions+10,
                    "total_articles":total_articles+1,
                    "today_total_articles":today_total_articles+1
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=articles_count_data)
        if contributions > 74 and contributions < 81:
            self.setNotification(user_id=user_id, notify_msg="You have reached 75 contributions")
        return "Added"

    def decrement_article_blog_counts(self, data):
        contributions = data["contributions"]
        today_total_blog_articles = data["today_total_blog_articles"]
        total_blog_articles = data["total_blog_articles"]
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
                    "contributions":contributions-5,
                    "total_blog_articles":total_blog_articles-1,
                    # "today_total_blog_articles":today_total_blog_articles+1
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=articles_count_data)
        return "Added"


    def increment_article_blog_counts(self, data):
        contributions = data["contributions"]
        today_total_blog_articles = data["today_total_blog_articles"]
        total_blog_articles = data["total_blog_articles"]
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
                    "contributions":contributions+10,
                    "total_blog_articles":total_blog_articles+1,
                    # "today_total_blog_articles":today_total_blog_articles+1
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=articles_count_data)
        if contributions > 74 and contributions < 81:
            self.setNotification(user_id=user_id, notify_msg="You have reached 75 contributions")
        return "Added"

    def decrement_article_counts(self, data):
        contributions = data["contributions"]
        today_total_articles = data["today_total_articles"]
        total_articles = data["total_articles"]
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
                    "contributions":contributions-5,
                    "total_articles":total_articles-1,
                    # "today_total_articles":today_total_articles-1
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=articles_count_data)
        return "Added"



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
            val = self.get_first_image(str=x['news'])
            x['tbnail'] = val["bytes"]
            x['tbfilename'] = val["filename"]
            x['time_ago'] = self.calculateHour(postdate=x['date'], posttime=x['time'])

        if len(data_in_list) < 11:
            return self.get_all_news_content()
        return data_in_list

    def blog_get(self):
        blogarticles = json.dumps({
            "collection": "blogarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=blogarticles)
        data_in_list = response.json()["documents"]
        data_in_list.reverse()
        for x in data_in_list:
            val = self.get_first_image(str=x['blog'])
            x['tbnail'] = val["bytes"]
            try:
             x['tbfilename'] = val["filename"][1:]
            except:
                pass
            x['description'] = self.get_description(html=x["blog"])
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

        # news___.reverse()
        return news___

    def get_users_articles(self, user_id):
        newsarticles = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "author_id":user_id,
                }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=newsarticles)
        articles = response.json()["documents"]
        todays_articles = []
        previous = []
        for i in articles:
            if i["date"] == datetime.datetime.now().strftime("%d-%m-%Y"):
                todays_articles.append(i)
            else:
                previous.append(i)
        return {
            "today":todays_articles,
            "previous":previous
        }

    def get_users_blog_article(self, user_id):
        blogarticles = json.dumps({
            "collection": "blogarticles",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "author_id":user_id,
                }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=blogarticles)
        articles = response.json()["documents"]
        todays_articles = []
        previous = []
        for i in articles:
            if i["date"] == datetime.datetime.now().strftime("%d-%m-%Y"):
                todays_articles.append(i)
            else:
                previous.append(i)
        return {
            "today":todays_articles,
            "previous":previous
        }

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
        news['time_ago'] = self.calculateHour(postdate=news['date'], posttime=news['time'])
        if news == None:
            return "blog"
        return news

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
        blog["description"] = self.get_description(html=blog["blog"])
        blog['time_ago'] = self.calculateHour(postdate=blog['date'], posttime=blog['time'])
        return blog

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
        self.decrement_article_counts(data=self.get_user_instance(user_id=user_id))
        return True

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
        self.decrement_article_blog_counts(data=self.get_user_instance(user_id=user_id))
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
        newdataids = json.dumps({
            "collection": "ids",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "id":"data",
                "usernames":prev_username,
            },
            "update":{
                "$set":{
                    "usernames.$":newusername
                }
            }
            })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=newdataids)
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

    def insert_todays_word(self, user_id, word, meaning):
        todaysword = json.dumps({
            "collection": "todaysword",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "id":"word-today"
            },
            "update":{
                "$set":{"user_id":user_id,
                "username":self.get_user_instance(user_id)["username"],
                "word":word,
                "meaning":meaning,
                "word_id":codeId().generate_id(),
                "date":datetime.datetime.now().strftime("%d-%m-%Y")
                }
            }
        })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=todaysword)
        return True

    def get_todays_word(self):
        todaysword = json.dumps({
            "collection": "todaysword",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "id":"word-today"
            }
        })
        response = requests.request("POST", url=self.findone, headers=self.header, data=todaysword)
        todays_word = response.json()["document"]
        return todays_word

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

        newdataids = json.dumps({
            "collection": "ids",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "id":"data",
                "heading_urls":prev_heading_url,
            },
            "update":{
                "$set":{
                    "heading_urls.$":newheadingurl
                }
            }
            })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=newdataids)
        return True

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
        newheading_url = GoogleTranslator(source='auto', target='en').translate(newheading_url)
        replaced_str = re.sub('[/<\/?^>+(>|$)/g]', "", blog)   
        total_words = len(replaced_str.split(" ")) 
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

        newdataids = json.dumps({
            "collection": "ids",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "id":"data",
                "heading_urls":prev_heading_url,
            },
            "update":{
                "$set":{
                    "heading_urls.$":newheading_url
                }
            }
            })
        response = requests.request("POST", url=self.updateone, headers=self.header, data=newdataids)
        return True

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

    def is_woftheday_stack_available(self):
        todaysword = json.dumps({
            "collection": "todaysword",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                "id":"word-today"
            }
        })
        response = requests.request("POST", url=self.findone, headers=self.header, data=todaysword)
        if response.json()["document"]["date"]==datetime.datetime.now().strftime("%d-%m-%Y"):
            return False
        return True

    def get_all_news_content(self):
        articles = json.dumps({
            "collection": "newsarticles",
            "database": "newsmain",
            "dataSource": "Cluster0"
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=articles)
        response__ = response.json()["documents"]
        response__.reverse()
        for x in response__:
            val = self.get_first_image(str=x['news'])
            x['tbnail'] = val["bytes"]
            x['tbfilename'] = val["filename"]
            x['time_ago'] = self.calculateHour(postdate=x['date'], posttime=x['time'])
        return response__

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
                            if val == 0:
                                val = 24 - (currenthour + posthour)

                            if val < 0:
                                val = -(val)
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
            todays_articles = []
            previous = []
            for i in comments:
             if i["date"] == datetime.datetime.now().strftime("%d-%m-%Y"):
                todays_articles.append(i)
             else:
                previous.append(i)
            return {
           "today":todays_articles,
            "previous":previous
            }
            
            
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
                "collection": "drafts",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "user_id":user_id,
                    "draft_id":draft_id,
                    }
                })
            response = requests.request("POST", url=self.deleteone, headers=self.header, data=draft)
            print(response.text)
            return True
        
    def getdraftsofUser(self, user_id):
            draft = json.dumps({
                "collection": "drafts",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "user_id":user_id
                },
            }) 
            response = requests.request("POST", url=self.find, headers=self.header, data=draft)
            drafts = response.json()["documents"]         
            print(drafts)                         
            if drafts == None:
                pass
            else:
                for i in drafts:
                    i["time_ago"] = self.calculateHour(postdate=i["date"], posttime=i["time"])
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
            
# BackEnd().setNotification(user_id="user_id", notify_msg="Your post was successfully uploaded")
# BackEnd().deleteNotifications(notify_id='Falof02343495167', user_id="user_id")
# BackEnd().deleteAllNotifications(user_id="user_id")
# BackEnd().getNotifcations(user_id="user_id")

    # def set_todays_statistics(self):
    #     user_instance = json.dumps({
    #         "collection": "users",
    #         "database": "newsmain",
    #         "dataSource": "Cluster0",
    #         "filter":{
    #             "user_id":user_id
    #         }
    #     })
    #     response = requests.request("POST", url=self.findone, headers=self.header, data=user_instance).json()["document"]

    #     return True



# BackEnd().createDraft(user_id="user_id")
# BackEnd().deletedraft(draft_id="nsLUP22201974382", user_id='lyNFw14482682664')