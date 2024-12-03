import requests

def get_headers():
    response = requests.get('https://httpbin.org/get') 
    return response.json()['headers']['Host']