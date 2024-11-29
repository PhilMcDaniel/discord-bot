import openai
import os
import config
import requests


#authenticate openai
openai.api_key = config.API_KEY


def get_aitext_completion(aitext_text_prompt):
    """retrives ai text from openai completion ai"""
    try:
        response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=aitext_text_prompt,
        max_tokens=1024,
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


#print(get_aiart_variation('https://cdn.britannica.com/35/7535-004-99D14F9B/Winston-Churchill-Yousuf-Karsh-1941.jpg')[0]['url'])