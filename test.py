import openai
import config
import os

print(os.getcwd())


openai.api_key = config.API_KEY


response = openai.Image.create(
prompt="a close up, studio photographic portrait of a white siamese cat that looks curious, backlit ears",
n=1,
size="512x512")

response = openai.Image.create_edit(
image=open("images\\otter2.PNG", "rb"),
mask=open("images\\otter2_mask.PNG", "rb"),
prompt="otter in yellow and blue water",
n=1,
size="512x512"
)

response = openai.Image.create_variation(
image=open("images\\shelby2.PNG", "rb"),
n=1,
size="512x512"
)

response['data'][0]['url']
