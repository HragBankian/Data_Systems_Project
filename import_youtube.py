
import pyodbc
from ytmusicapi import YTMusic
import os
ytmusic = YTMusic("oauth.json")

# Function to insert data into SQL table
def insert_into_sql_table(cursor, title, artist):
    insert_query = "INSERT INTO YourTable (Title, Artist) VALUES (?, ?)"
    cursor.execute(insert_query, title, artist)
    cursor.commit()

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

# Perform search
search_results = ytmusic.search("Oasis Wonderwall", filter="songs")
print(search_results)
