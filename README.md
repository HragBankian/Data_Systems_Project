# Data Systems Project
Project completed in the context of SOEN 363 using tools such as MySQL and Neo4j.
## Spotify API fetching
https://www.youtube.com/watch?v=WAmEZBEeNmg

``` Package you might need to install
python -m pip install python-dotenv 
1. You need to create a .env file in the root directory
2. Add the following lines in the .env file
CLIENT_ID= 'Your Spotify Client ID'
CLIENT_SECRET= 'Your Spotify Client Secret'
3. Save the file
4. Run the code by doing python import_spotify.py
```

## Youtube API fetching 
https://ytmusicapi.readthedocs.io/en/stable/index.html

Make sure you have installed ytmusicapi 
``` 
python -m pip install ytmusicapi
```

```python

Run ytmusicapi oauth in terminal to connect to google account

```
## Data Manipulation
```python
## API Spotify fetching
https://engineering.atspotify.com/2015/03/understanding-spotify-web-api/#:~:text=You%20can%20make%20similar%20calls,that%20it's%20free%20to%20access.

## Database must add the following 
INSERT INTO media_types VALUES (1,'MUSIC_VIDEO_TYPE_ATV');
INSERT INTO media_types VALUES (2,'show');
