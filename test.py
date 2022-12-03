import openai
import config


openai.api_key = config.API_KEY

try:
    response = openai.Image.create(
    prompt="testing bar strength trump",
    n=1,
    size="512x512")

    response['data'][0]['url']

except openai.InvalidRequestError:
    print("Your prompt contained text that was not allowed by the openai safety system.")