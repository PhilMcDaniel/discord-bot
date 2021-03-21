def get_URL(platform,platformid):
    """Get the URL that needs to be parsed"""
    url = f"https://rocketleague.tracker.network/rocket-league/profile/{platform}/{platformid}/overview"
    return url
#get_URL("steam","76561198040589211")