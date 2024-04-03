
import pyodbc
from ytmusicapi import YTMusic
import os
ytmusic = YTMusic("oauth.json")
import mysql.connector

# Replace with your local MySQL connection within the env file
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

# Establish database connection
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)


cursor = conn.cursor()


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

artists = [
    "Taylor Swift", "Ed Sheeran", "Beyoncé", "Adele", "Drake", 
    "Coldplay", "Ariana Grande", "Eminem", "Rihanna", "Justin Bieber", 
    "Katy Perry", "The Weeknd", "Bruno Mars", "Lady Gaga", "Kanye West", 
    "Maroon 5", "Sam Smith", "Shawn Mendes", "Nicki Minaj", "Imagine Dragons", 
    "Post Malone", "Sia", "John Legend", "One Direction", "Dua Lipa", 
    "Pink", "Twenty One Pilots", "The Chainsmokers", "Zayn", "Miley Cyrus", 
    "Calvin Harris", "Lana Del Rey", "Michael Jackson", "Selena Gomez", 
    "Linkin Park", "Kendrick Lamar", "Justin Timberlake", "Travis Scott", 
    "Shakira", "Britney Spears", "Camila Cabello", "Chris Brown", 
    "Halsey", "Queen", "Lorde", "Foo Fighters", "Billie Eilish", 
    "Jason Derulo", "Lil Wayne", "P!nk", "David Bowie", "Elton John", 
    "Alicia Keys", "Metallica", "Eagles", "U2", "Madonna", "Prince",
    "A$AP Rocky", "Blackpink", "Guns N' Roses", "The Beatles", 
    "Bob Dylan", "The Rolling Stones", "Jay-Z", "Red Hot Chili Peppers", 
    "Khalid", "Tame Impala", "Van Halen", "Green Day", "Radiohead", 
    "Backstreet Boys", "Eminem", "Childish Gambino", "Led Zeppelin", 
    "The Weeknd", "Outkast", "Pink Floyd", "BTS", "Fleetwood Mac", 
    "Pearl Jam", "The Notorious B.I.G.", "Usher", "Snoop Dogg", 
    "Oasis", "Gorillaz", "Blink-182", "The Cure", "Nirvana", 
    "Beck", "Arctic Monkeys", "Foo Fighters", "Metallica", 
    "Paramore", "The Strokes", "Lil Uzi Vert", "Jimi Hendrix", 
    "Frank Ocean", "Daft Punk", "The Who", "AC/DC", "Dr. Dre"
]

# Loop through each artist
for artist in artists:
    # Searching for songs by the artist
    podcast_results = ytmusic.search(artist, filter="songs")

    # Inserting the data into the database
    for result in podcast_results:
        cursor.execute("INSERT INTO songs (song_name, artist_name, album, duration, media_type_id) VALUES (%s, %s, %s, %s, %s)", (result['title'], result['artists'][0]['name'], result['album']['name'], result['duration_seconds'], 1))
        conn.commit()

# Fetching the data from the database
cursor.execute("SELECT * FROM songs")
result = cursor.fetchall()
for row in result:
    print(row)

# Closing the connection
cursor.close()


