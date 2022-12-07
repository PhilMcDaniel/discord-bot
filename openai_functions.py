import openai
import os
import config

#authenticate openai
openai.api_key = config.API_KEY

def get_moderation_category_scores(text_prompt):
    """retrives moderation category scores from openai moderation API"""
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


