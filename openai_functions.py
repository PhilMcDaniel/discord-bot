from openai import OpenAI
import os
import config
import requests

import re

#authenticate openai
client = OpenAI(api_key=config.API_KEY)

def get_aitext_completion(aitext_text_prompt, developer_prompt=None):
    """
    Retrieves AI text from OpenAI's chat completions.
    
    Parameters:
        aitext_text_prompt (str): The primary prompt sent as the "user" message.
        developer_prompt (str, optional): Additional prompt instructions sent as the "developer" message.
    
    Returns:
        str: The AI's completion text.
    """
    # Always include the user's prompt.
    messages = [{"role": "user", "content": aitext_text_prompt}]
    
    # Optionally add the developer prompt if provided.
    if developer_prompt is not None:
        messages.append({"role": "developer", "content": developer_prompt})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=2048,
            n=1
        )
        return response.choices[0].message.content
    except Exception as err:
        raise

#get_aitext_completion('Tell me a short moral story in a haiku')

def split_at_punctuation(text, threshold=1500, max_length=10000):
    chunks = []
    start = 0

    while start < len(text):
        # Find the next chunk within the allowed range
        end = min(start + max_length, len(text))
        substring = text[start:end]

        # Look for the first punctuation after the threshold
        match = re.search(r'[.!?]', substring[threshold:])
        if match:
            split_point = start + threshold + match.start() + 1
        else:
            # No punctuation found, split at max_length
            split_point = end

        # Add the chunk
        chunks.append(text[start:split_point].strip())
        start = split_point

    return chunks

def get_aiimage(aiart_text_prompt):
    """generates an image using the openai image generation api"""
    try:
        response = client.images.generate(
        model="dall-e-3",
        prompt=f"{aiart_text_prompt}",
        size="1024x1024",
        quality="standard",
        n=1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as err:
        #return print(f"Unexpected {err=}, {type(err)=}")
        raise
    except OpenAI.OpenAIError as e:
        print(e.http_status)
        print(e.error)
#image = get_aiimage('test image')
#image