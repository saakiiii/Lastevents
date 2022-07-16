import os
import pathlib
from PIL import Image, ImageDraw, ImageFont

text = """Registrations for the Agneepath scheme.
   Almost 43000 job vacancies are offered by the army and navy services. Indian airforce to start registrations for the Agneepath scheme on June 24. There are 3000 available job places in Airforce.""" 
new_text = ""
original_text = text.split(' ')
print(original_text)
count = 1
for i in original_text:
    if count % 7 == 0:
        new_text = new_text + '\n'
        print(new_text)
    new_text = new_text + " " + i
    count += 1

print(new_text)        
image = Image.open('postbg1.jpg')
print(image.size)
WIDTH = image.size[0]
HEIGHT = image.size[1]
imagedraw = ImageDraw.Draw(image)
font = ImageFont.truetype(r"verdana.ttf", 60)
print(imagedraw.textsize(text, font=font))
width, height = imagedraw.textsize(new_text, font=font) 
imagedraw.text(((WIDTH-width)/2 + 15, (HEIGHT-height)/2), text=new_text, fill="white", align="center", font=font)
# image.show()
image.save("new.png")
os.remove('new.png')
# image = Image.open("download.jpg")
# image.thumbnail((168, 225))
# image.show()
# print(len("60 characters is between 8 words and 15 words with spaces included in the character count. If space "))