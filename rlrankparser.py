import requests
from bs4 import BeautifulSoup

def get_url(platform,platformid):
    """Get the URL that needs to be parsed"""
    url = f"https://rocketleague.tracker.network/rocket-league/profile/{platform}/{platformid}/overview"
    return url
#get_URL("steam","76561198040589211")

url = get_url("steam","76561198040589211")
print(url)

def parse_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    title = soup.select("title")
    #print(title)
    data = soup.select("script")
    #print(data)
    return title,data
parse_url(get_url("steam","76561198040589211"))
