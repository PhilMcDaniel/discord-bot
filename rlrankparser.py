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

    #user metadata (name,platform,id)
    username = api_response['data']['platformInfo']['platformUserHandle']
    platform = api_response['data']['platformInfo']['platformSlug']
    platformid = api_response['data']['platformInfo']['platformUserIdentifier']
    user_info = f"Platform: {platform}, Platform ID: {platformid}, Username: {username}"
    
    #found by using .keys() down the json response tree
    #2v2 data
    playlist = api_response['data']['segments'][3]['metadata']['name']
    rank = api_response['data']['segments'][3]['stats']['tier']['metadata']['name']
    division = api_response['data']['segments'][3]['stats']['division']['metadata']['name']
    mmr = api_response['data']['segments'][3]['stats']['rating']['value']
    twos_data = f"Playlist: {playlist}, Rank: {rank} - {division}, MMR: {mmr}"
    

    #3v3 data
    playlist = api_response['data']['segments'][4]['metadata']['name']
    rank = api_response['data']['segments'][4]['stats']['tier']['metadata']['name']
    division = api_response['data']['segments'][4]['stats']['division']['metadata']['name']
    mmr = api_response['data']['segments'][4]['stats']['rating']['value']
    threes_data = f"Playlist: {playlist}, Rank: {rank} - {division}, MMR: {mmr}"
    

    response = f"{user_info} | {twos_data} | {threes_data}"
    return(response)
    
    
#get_rank_from_api(form_url('steam','76561198040589211'))