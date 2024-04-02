
import pyodbc
from ytmusicapi import YTMusic
import os
ytmusic = YTMusic("oauth.json")

#Assuming you want to search for "Self Help" Podcasts
def search_podcasts(query):
    search_results = ytmusic.search(query,filter="podcasts")
    return search_results

#Assuming you want to search songs by "Taylor Swift"
def search_songs(query):
    search_results = ytmusic.search(query,filter="songs")
    return search_results

# Initialize YTMusic object
ytmusic = YTMusic("oauth.json")

podcast_results = ytmusic.search("Gwen Stefani", filter="songs")
# print(podcast_results)
for result in podcast_results:
    print(f"title : {result['title']}")
    print(f"artists: {result['artists'][0]['name']}")
    print(f"album: {result['album']['name']}")
    print(f"duration: {result['duration_seconds']}")
    print ("\n\n")


