import requests
import json
def r_memes():
    url = "https://meme-api.com/gimme/memes"
    r = requests.get(url)
    byte_data = r.content
    json_str = byte_data.decode('utf-8')

    data = json.loads(json_str)
    value = data['url']

    return value


def r_nsfw_meme():
    url = "https://meme-api.com/gimme/nsfw_meme"
    r = requests.get(url)
    byte_data = r.content
    json_str = byte_data.decode('utf-8')

    data = json.loads(json_str)
    value = data['url']

    return value

def r_dankmemes():
    url = "https://meme-api.com/gimme/dankmemes"
    r = requests.get(url)
    byte_data = r.content
    json_str = byte_data.decode('utf-8')

    data = json.loads(json_str)
    value = data['url']

    return value
