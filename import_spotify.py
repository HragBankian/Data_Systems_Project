from dotenv import load_dotenv
import os
import base64
from requests import post,get
import json

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    url = "https://accounts.spotify.com/api/token"
    headers = {
         "Authorization" : "Basic " + auth_base64,
         "Content-Type" : "application/x-www-form-urlencoded"
    }
    data ={"grant_type" : "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

def get_music_tracks(token, query):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {
        "q": query,
        "type": "track",
        "market": "US",
        "limit": 10 
    }
    result = get(url, headers=headers, params=params)
    json_result = json.loads(result.content)
    return json_result

def get_podcasts(token, query):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {
        "q": query,
        "type": "show",
        "market": "US",
        "limit": 10  # Limiting to 10 results for demonstration purposes
    }
    result = get(url, headers=headers, params=params)
    json_result = json.loads(result.content)
    return json_result

# Example usage:
token = get_token()
# music_tracks = get_music_tracks(token, "pop music")
# print(music_tracks)
podcasts = get_podcasts(token, "tech podcasts")
print(podcasts)
