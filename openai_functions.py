from openai import OpenAI
import os
import config
import requests


#authenticate openai
client = OpenAI(api_key=config.API_KEY)

def get_aitext_completion(aitext_text_prompt):
    """retrives ai text from openai completion ai"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                    {"role": "user", "content": f"{aitext_text_prompt}"}
                    ],
            max_tokens=2048,
            n=1
        )
        return response.choices[0].message.content
    except Exception as err:
        #return print(f"Unexpected {err=}, {type(err)=}")
        raise
    except:
        pass
#get_aitext_completion('Tell me a short moral story in a haiku')


#print(get_aiart_variation('https://cdn.britannica.com/35/7535-004-99D14F9B/Winston-Churchill-Yousuf-Karsh-1941.jpg')[0]['url'])