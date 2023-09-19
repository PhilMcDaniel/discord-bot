import openai
import os
import config
import requests
from PIL import Image
from io import BytesIO

#authenticate openai
openai.api_key = config.API_KEY

def get_moderation_category_scores(text_prompt):
    """returns moderation category scores from openai moderation API"""
    try:
        moderation_response = openai.Moderation.create(input=text_prompt)
        #category scores
        return moderation_response['results'][0]['category_scores']
    except Exception as err:
        #return print(f"Unexpected {err=}, {type(err)=}")
        raise
    except:
        pass
#result = get_moderation_category_scores("what really is a naughty word?")

def get_aiart(ai_art_text_prompt):
    """returns ai art from the openai image api based on the prompt"""
    try:
        response = openai.Image.create(
        prompt=ai_art_text_prompt,
        n=2,
        size="512x512")
    
        return response['data']
    except Exception as err:
        #return print(f"Unexpected {err=}, {type(err)=}")
        raise
    except:
        pass
#get_aiart('the ink spots cover art')

def get_aitext_completion(aitext_text_prompt):
    """retrives ai text from openai completion ai"""
    try:
        response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=aitext_text_prompt,
        max_tokens=512,
        n=1,
        stream=False
        )
        return response['choices'][0]['text']
    except Exception as err:
        #return print(f"Unexpected {err=}, {type(err)=}")
        raise
    except:
        pass
#get_aitext_completion('What python 3 code is needed to read an image from a URL using the requests library?')


#TODO AIART create_edit


#TODO AIART create_variation


def get_aiart_variation(url):
    """Gets image from url, resizes to square and saves locally to .png. Generates image using openai create_variation"""
    img_folder = os.path.join(os.getcwd(),'images')
    file_name = 'srcimg.png'
    fullpath = os.path.join(img_folder,file_name)

    #delete all files in images folder
    for f in os.listdir(img_folder):
        os.remove(os.path.join(img_folder, f))

    #get url response
    try:
        img_url = url
        response = requests.get(img_url)
        # Open the image
        img = Image.open(BytesIO(response.content))
    except:
        raise Exception("Error retrieving image from URL")

    #resize image to square
    width, height = img.size
    min_size = min(width,height)
    img = img.resize((min_size,min_size),resample=0)

    #save image as .png in local folder
    img.save(fullpath)

    #generate variation from openai
    response = openai.Image.create_variation(
    image=open(fullpath, "rb"),
    n=2,
    size="512x512"
    )
    return response['data']

#print(get_aiart_variation('https://cdn.britannica.com/35/7535-004-99D14F9B/Winston-Churchill-Yousuf-Karsh-1941.jpg')[0]['url'])