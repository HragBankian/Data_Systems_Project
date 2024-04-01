
import pyodbc
from ytmusicapi import YTMusic
import os
ytmusic = YTMusic("oauth.json")
def connect_to_sql_server():
    conn = pyodbc.connect('DRIVER={SQL Server};'
                          'SERVER=' + os.getenv('DB_SERVER') + ';'
                          'DATABASE=' + os.getenv('DB_DATABASE') + ';'
                          'UID=' + os.getenv('DB_UID') + ';'
                          'PWD=' + os.getenv('DB_PASSWORD'))
    return conn.cursor()

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

# Connect to SQL Server
cursor = connect_to_sql_server()

# Parse JSON data and insert into SQL table
for result in search_results:
    title = result['title']
    artist = result['artists'][0]['name']
    insert_into_sql_table(cursor, title, artist)

# Close the cursor and connection
cursor.close()