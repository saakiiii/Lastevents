from backend import BackEnd

class SearchApi:
    
    def __init__(self) -> None:
        pass
    
    def Search(self, text, heading_urls=BackEnd().get_heading_urls()):
        li = []
        for i in heading_urls:
            if text.lower() in i.lower().replace("-", " "):
                li.append(i) 
        
        return li
        
# heading_urls = ["hellow word", "adfaf", "wolf"]
# SearchApi().Search(heading_urls=heading_urls, text="wol")