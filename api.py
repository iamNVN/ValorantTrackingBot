import requests

def player_exists(name,tag):
    r = requests.get(f'https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}')
    if r.status_code == 200:
        return r.json()['data']['region']
    return False

def player_last_match(player,region):
    a = player.split('#')
    name = a[0]
    tag = a[1]
    r = requests.get(f'https://api.henrikdev.xyz/valorant/v1/lifetime/matches/{region}/{name}/{tag}?size=1')
    if r.status_code == 200:
        return r.json()['data'][0]
    return None
