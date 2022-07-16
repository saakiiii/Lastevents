from TwitterApi import TwitterApi
from InstaApi import InstaApi
import requests
import json
from deep_translator import GoogleTranslator
from LinkedinPost import LinkedinPost

from backend import BackEnd

class AutoMation(BackEnd):

    def __init__(self) -> None:
       super().__init__()
       pass

    def getRecents(self):
        recents = json.dumps({
            "collection": "recents",
            "database": "newsmain",
            "dataSource": "Cluster0",
            "filter":{
                 "id":"data",
            }
        })
        response = requests.request("POST", url=self.find, headers=self.header, data=recents)
        # print(response.json())
        heading_urls = [x["heading_url"] for x in response.json()["documents"]]
        # print(heading_urls)
        self.publishPosts(heading_urls=heading_urls)

    def deleteRecentOneByOne(self, heading_urls=[]):
        for i in heading_urls:
            recents = json.dumps({
                "collection": "recents",
                "database": "newsmain",
                "dataSource": "Cluster0",
                "filter":{
                    "heading_url":i,
                }
                })
            response = requests.request("POST", url=self.deleteone, headers=self.header, data=recents)
            print(response.text)

    def Tweet(self, text, poll_options=None, poll_duration_minutes=None, direct_message_deep_link=None):
        print(text)
        TwitterApi().Tweet(text=text,
                           poll_options=poll_options,
                           poll_duration_minutes=poll_duration_minutes,
                           direct_message_deep_link=direct_message_deep_link,
                           )

    def Insta(self, text, link):
        InstaApi().upload_photo(text=text, link=link)

    def publishPosts(self, heading_urls=[]):
        articles = self.get_articles_by_heading_url(heading_urls=heading_urls)
        for i in articles:
          try:
            heading = i["heading"]
            heading_url = i["heading_url"]
            # print(heading)
            # print(heading_urls)
            heading = GoogleTranslator(source='auto', target='en').translate(heading)
            self.Tweet(text=heading + f" www.lastevents.space/news/read/view/{heading_url}")
            # self.Insta(text=heading, link=f'www.lastevents.space/{heading_url}')
            LinkedinPost().post_lindedin(message=heading, link=f"www.lastevents.space/news/read/view/{heading_url}", link_text=heading)
          except:
              pass
        self.deleteRecentOneByOne(heading_urls=heading_urls)

# AutoMation().Tweet("One of the test email 3049820sda0sadf0as8df09s")
# AutoMation().Insta(text="hello world")
AutoMation().getRecents()