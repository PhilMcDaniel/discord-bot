import openai
import os
import config

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
        model="text-davinci-003",
        prompt=aitext_text_prompt,
        max_tokens=256,
        n=1,
        stream=False
        )
        return response['choices'][0]['text']
    except Exception as err:
        #return print(f"Unexpected {err=}, {type(err)=}")
        raise
    except:
        pass
#get_aitext_completion('What is the meaning of life?')


#TODO AIART create_edit

#TODO AIART create_variation