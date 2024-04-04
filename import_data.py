from dotenv import load_dotenv
import os
import base64
from requests import post,get
import json
import mysql.connector
from ytmusicapi import YTMusic

# Database configuration
DB_HOST = 'XYZ'
DB_USER = 'XYZ'
DB_PASSWORD = 'XYZ'
DB_DATABASE = 'XYZ'
# Establish database connection
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)

cursor = conn.cursor()

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
        "limit": 20
    }
    result = get(url, headers=headers, params=params)
    json_result = json.loads(result.content)
    return json_result

# Intializing the token
token = get_token()

# Categories for podcast topics
podcast_topics = [
    "Technology trends in 2024",
    "The future of artificial intelligence",
    "Exploring sustainable living practices",
    "Interviews with successful entrepreneurs",
    "Climate change and its impact on society",
    "The history of ancient civilizations",
    "Space exploration and colonization",
    "Mental health awareness and coping strategies",
    "Financial literacy and investment tips",
    "Nutrition and healthy eating habits",
    "The psychology of decision-making",
    "Famous conspiracy theories and myths",
    "The rise of e-sports and gaming culture",
    "Unsolved mysteries from around the world",
    "Social media's influence on modern society",
    "DIY projects and home improvement tips",
    "Understanding quantum mechanics",
    "World travel adventures and experiences",
    "Effective communication techniques",
    "Exploring different meditation practices",
    "Entrepreneurship in the digital age",
    "The art of storytelling",
    "Personal development and self-improvement",
    "The future of work and remote jobs",
    "Discussing famous literature and authors",
    "Climate change solutions and innovations",
    "Healthcare advancements and breakthroughs",
    "The impact of automation on industries",
    "History's most notorious criminals",
    "Navigating relationships and dating in the modern world",
    "Cultural diversity and inclusivity",
    "The science of happiness and well-being",
    "Exploring different philosophical ideologies",
    "Cryptocurrency and blockchain technology",
    "True crime stories and investigations",
    "Innovations in renewable energy",
    "The psychology of motivation and productivity",
    "Documentary-style deep dives into historical events",
    "The future of transportation",
    "SpaceX and the race to Mars",
    "The art of photography and visual storytelling",
    "Understanding the human brain and cognition",
    "Sustainable fashion and ethical consumerism",
    "Conspiracy theories debunked",
    "Exploring different world cuisines",
    "The science of sleep and dreams",
    "The psychology of fear and anxiety",
    "Leadership lessons from successful CEOs",
    "The rise of mindfulness and meditation",
    "Futuristic technologies and their implications",
    "The mysteries of the deep ocean",
    "The psychology of addiction and recovery",
    "The history of famous landmarks and monuments",
    "Effective time management strategies",
    "The future of education and learning",
    "Ancient myths and legends from different cultures",
    "Space tourism and commercial space travel",
    "Innovations in healthcare technology",
    "Understanding climate change skepticism",
    "The intersection of art and technology",
    "The psychology of persuasion and influence",
    "Exploring different forms of art therapy",
    "The impact of social media influencers",
    "The history of ancient civilizations",
    "Exploring the world of virtual reality",
    "Breaking down complex scientific concepts",
    "The science behind popular diets and nutrition trends",
    "Famous historical figures and their legacies",
    "The future of genetic engineering",
    "The psychology of creativity and innovation",
    "The rise of plant-based diets",
    "Unexplained phenomena and supernatural occurrences",
    "The history of famous inventions",
    "Effective stress management techniques",
    "The psychology of decision-making",
    "The future of renewable energy",
    "Exploring different forms of art and expression",
    "The science of climate change",
    "The art of negotiation and conflict resolution",
    "Space exploration and the search for extraterrestrial life",
    "The history of major world religions",
    "The psychology of resilience and perseverance",
    "Exploring different forms of music therapy",
    "The impact of technology on mental health",
    "The future of augmented reality",
    "The mysteries of the human mind",
    "The history of major wars and conflicts",
    "The psychology of happiness and fulfillment",
    "The future of sustainable agriculture",
    "Innovations in medical treatments and procedures",
    "The art of public speaking and communication",
    "The psychology of success and achievement",
    "Exploring different forms of traditional medicine",
    "The future of space exploration",
    "The impact of globalization on cultures",
    "The psychology of love and relationships",
    "The rise of renewable energy sources",
    "The history of famous art movements",
    "Effective parenting strategies in the digital age",
    "The science of aging and longevity",
    "The future of artificial intelligence ethics",
    "Exploring different forms of dance therapy",
    "The psychology of trauma and healing",
    "The history of major scientific discoveries",
    "The impact of social media on mental health",
    "The future of clean energy technology",
    "Exploring different forms of creative writing",
    "The psychology of emotional intelligence",
    "The history of major epidemics and pandemics",
    "The future of transportation technology"
]
# podcasts = get_podcasts(token, podcast_topics[0])
# print(podcasts["shows"]["items"][0]['available_markets'][0])

# Loop through each artist
count = 1 
for topic in podcast_topics:
    # Searching for songs by the artist
    podcasts = get_podcasts(token, topic)

    # Inserting the data into the database
    for result in podcasts["shows"]["items"]:
        cursor.execute("INSERT INTO media_types (media_type) VALUES (%s)", ('podcast',))
        cursor.execute("INSERT INTO podcasts (podcast_id, podcast_name, publisher, overview, total_episodes) VALUES (%s, %s, %s, %s, %s)", (count, result['name'][:255], result['publisher'][:255], result['description'][:255], result['total_episodes']))
        for i in result['available_markets'] :
            cursor.execute("INSERT INTO available_markets (podcast_id, market_name) VALUES (%s,%s)", (count, i))
        count += 1
        conn.commit()

# Fetching the data from the database
cursor.execute("SELECT * FROM podcasts")
result = cursor.fetchall()
for row in result:
    print(row)

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
# its done :)
# Loop through each artist
for artist in artists:
    # Searching for songs by the artist
    podcast_results = ytmusic.search(artist, filter="songs")

    # Inserting the data into the database
    for result in podcast_results:
        if result is None:
            break
        cursor.execute("INSERT INTO media_types (media_type) VALUES (%s)", ("song",))
        cursor.execute("INSERT INTO songs (song_id,song_name, artist_name, album, duration) VALUES (%s,%s, %s, %s, %s)", (count,result['title'], result['artists'][0]['name'], result['album']['name'], result['duration_seconds']))
        count += 1
        conn.commit()

# Fetching the data from the database
cursor.execute("SELECT * FROM songs")
result = cursor.fetchall()
for row in result:
    print(row)


# Closing the connection
cursor.close()
