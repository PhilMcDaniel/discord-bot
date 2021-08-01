import requests
from bs4 import BeautifulSoup
import json

from requests import api

def form_url(platform,platformid):
    """Get the URL that needs to be parsed"""
    url = f"http://api.tracker.gg/api/v2/rocket-league/standard/profile/{platform}/{platformid}"
    return url
#form_url('steam','76561198040589211')

def get_rank_from_api(url):
    """sends request to API URL, returns data about player rank"""
    #read from chrome devtools network details
    headers = {
    'Accept': 'application/json, text/plain, */*'
    ,'Accept-Language': 'en'
    ,'DNT': '1'
    ,'Referer': 'https://rocketleague.tracker.network/'
    ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    api_response = requests.get(url,headers=headers)
    api_response = api_response.json()
    
    #get user info
    username = api_response['data']['platformInfo']['platformUserHandle']
    platform = api_response['data']['platformInfo']['platformSlug']
    platformid = api_response['data']['platformInfo']['platformUserIdentifier']
    user_info = f"Platform: {platform}, Platform ID: {platformid}, Username: {username}"
    response_list=[]
    response_list.append(user_info)
    for key in api_response['data']['segments']:
        #lifetime doesn't have normal keys
        if key['metadata']['name']=='Lifetime':
            pass
        else:
            playlist = key['metadata']['name']
            rank = key['stats']['tier']['metadata']['name']
            division = key['stats']['division']['metadata']['name']
            mmr = key['stats']['rating']['value']
            response_list.append(f"Playlist: {playlist}, Rank: {rank}-{division}, MMR: {mmr}")
    
    return(response_list)
#get_rank_from_api(form_url('steam','76561198040589211'))