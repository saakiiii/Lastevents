from backend import BackEnd

class SearchApi:
    
    def __init__(self) -> None:
        pass
    
    def Search(self, text, heading_urls=BackEnd().get_news_and_blog_articles()):
        li = []
        for i in heading_urls:
            if text.lower() in i["heading"].lower():
                li.append(i) 
        
        return li
        
# heading_urls = ["hellow word", "adfaf", "wolf"]
# SearchApi().Search(heading_urls=heading_urls, text="wol")
# print(SearchApi().Search("h"))