import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import mysql.connector

# set up authentication

client_id = "bceacca66ac043b1a6d710f362b6d7b8"       # Replace with your Client ID
client_secret = "ad46077c60f440d3b4d890ad855f1ecd"   # Replace with your Client Secret

# Create a credentials manger
auth_manager = SpotifyClientCredentials(
    client_id = client_id,
    client_secret = client_secret
)

# Initailize spotify with auth
sp= spotipy.Spotify(auth_manager = auth_manager)

#MySQL Database Connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'spotify_dp'
}

# connect to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Read track URLs form file
file_path = "track_urls.txt"
with open(file_path,'r') as file:
    track_urls = file.readlines()

#process each URL
for track_url in track_urls:
    track_url = track_url.strip() # Remove and leading /trailling whitespace
    try:
        # Extract track ID from URL
        track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

        # Fetch track details from Soptify API
        track = sp.track(track_id)

        # Extract metadatas
        track_data ={
            'Track Name' : track['name'],
            'Artist' : track['artists'][0]['name'],
            'Album' : track['album']['name'],
            'Popularity' : track['popularity'],
            'Duration (minutes)' : track['duration_ms'] / 60000
        }

        # Insert query into MySQL 
        insert_query = """
        INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            track_data['Track Name'],
            track_data['Artist'],
            track_data['Album'],
            track_data['Popularity'],
            track_data['Duration (minutes)']  
        ) )
        connection.commit()

        print(f"Inserted: {track_data['Track Name']} by {track_data['Artist']}")

    except Exception as e:
        print(f"ERROR Processing URL: {track_url}, Error: {e}")

#close the connection 
cursor.close()
connection.close()

print("All tracks have been processed and inserted into the databases.")
        
