from inspect import unwrap
from bs4 import BeautifulSoup
from googletrans import Translator
# from google_trans_new import google_translator  
import re
import openai
import random 
import asyncio
from PIL import Image
from playsound import playsound
import time
import pygetwindow as gw    

async def display_image_and_play_sound(image_path, sound_path):
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, playsound, sound_path)

    # Delay the execution to allow the sound to start playing
    await asyncio.sleep(0)

    # Open and display the image using PIL
    image = Image.open(image_path)
    image.show()

    # image_window = gw.getWindowsWithTitle(image.filename)[0]
    # image_window.activate()

class ChatApp:
    def __init__(self):
        # Setting the API key to use the OpenAI API
        openai.api_key = "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"
        self.messages = [
            {"role": "system", "content": """I'm going to give you mathematical text and you need to translate them to norwegian. Please leave the math inside "\(" and "\)" as is."""}, {},
        ]

    def chat(self, message):
        self.messages[1] = {"role": "user", "content": message}
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        return response["choices"][0]["message"]["content"]

# t = Translator()
t = ChatApp()

def gptTranslateTagCont(tag):
    finalString = ""
    for c in tag.contents:
        finalString = finalString + str(c) + " "
    return t.chat(finalString)

def spanRemover(soup):      # Remove previous spans
    spans = soup.find_all('span')
    for i in spans:
        sp = soup.span.unwrap()

def spanInsert(tag):
    # if not tag.string:
    #     return str(tag)
    # norwegian = '''\n <span class="multilang" lang="no">''' + translateTagCont(tag) + '</span'
    list_string = str(tag).split('>')
    list_string.insert(1, '''<span class="multilang" lang="en"''')
    half = '>'.join(list_string)
    
    half_string_list = half.split("<")
    half_string_list.insert(-1, '''/span> \n <span class="multilang" lang="no">''' + gptTranslateTagCont(tag) + '</span>')
    return '<'.join(half_string_list)

def googleTranslateTagCont(tag):
    finalString = ""
    for c in tag.contents:
        if str(c)[0] == "\\" or not str(c).strip():
            finalString = finalString + str(c) + " "
        else:
            finalString = finalString + t.translate(str(c), src="en", dest="no").text + " "
    return finalString

def translateHTMLCode(filename):

    with open(filename) as fp:
        soup = BeautifulSoup(fp, "html.parser")

    spanRemover(soup)

    tagsTBT = ["h3", "h4", "p"]#, "li"]
    for tag in tagsTBT:
        paras = soup.find_all(tag)
        for par in paras:
            pars = spanInsert(par)
            par.replace_with(BeautifulSoup(pars, "html.parser"))

    o = open("output.html", "w", encoding='utf-8')
    o.write(str(soup))
    o.close()

# new_span    = soup.new_tag("span", **{'class':'multilang'}, lang="en")
# new_span_no = soup.new_tag("span", **{'class':'multilang'}, lang="no")
soundbytes = ["1.mp3","2.mp3"]
picture_dex = ["1.png","2.jpg"]
try:
    translateHTMLCode("input.html")
except openai.error.RateLimitError as e:
    print("Error! Please try again later.")
    playsound(soundbytes[0])
else:
    print("Translated successfully!")
rand = random.randint(0,1)
asyncio.run(display_image_and_play_sound(picture_dex[1], soundbytes[1]))


# string = '''To find the vector \(\overrightarrow{AB}\) we simply subtract the position vector or \(A\) from the position vector of \(B\):'''
# test = re.split(r"\(", string)
# print(test)