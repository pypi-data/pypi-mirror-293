import requests
import json

def v1():
    url = "https://www.uuidtools.com/api/generate/v1"
    r = requests.get(url)
    byte_data = r.content
    json_str = byte_data.decode('utf-8')

    data = json.loads(json_str)
    value = data

    return value

def v4():
    url = "https://www.uuidtools.com/api/generate/v4"
    r = requests.get(url)
    byte_data = r.content
    json_str = byte_data.decode('utf-8')

    data = json.loads(json_str)
    value = data

    return value

