
import time
from instabot import Bot
import os
from PIL import Image, ImageDraw, ImageFont

from codegenerator import codeId

api = Bot()

class InstaApi:
    
    def __init__(self):
        pass
            
    def upload_photo(self, text, link=""):
        api.login(username="lastevents.space", password="lenovag40")
        image_id = self.createImage(text=text)
        time.sleep(5)
        os.rename(f'{image_id}.png', f'{image_id}.JPEG')
        time.sleep(2)
        if image_id != None: 
         api.upload_photo(photo=f"{image_id}.jpeg", caption=text)
         os.remove(f'{image_id}.jpeg')
         os.removedirs("config")
        else:
          pass
        
    def createImage(self, text):
        image_id = codeId().generate_image_id()
        new_text = ""
        original_text = text.split(' ')
        count = 1
        for i in original_text:
            if count % 7 == 0:
                new_text = new_text + '\n'
                print(new_text)
            new_text = new_text + " " + i
            count += 1  
        print(new_text)
        image = Image.open('postbg1.jpg')
        WIDTH = image.size[0]
        HEIGHT = image.size[1]
        imagedraw = ImageDraw.Draw(image)
        font = ImageFont.truetype(r"verdana.ttf", 60)
        width, height = imagedraw.textsize(new_text, font=font) 
        imagedraw.text(((WIDTH-width)/2 + 15, (HEIGHT-height)/2), text=new_text, fill="white", align="center", font=font)
        image.convert('RGB')
        image.save(f"{image_id}.png")
        
        return image_id

      
# InstaApi().upload_photo(text="This is the sample heading for the instagram post")
# image.show()
