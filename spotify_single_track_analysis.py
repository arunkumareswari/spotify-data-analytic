from spotipy.oauth2 import SpotifyClientCredentials  # oauth2 - open authorization 2.0 is an industry-standard protocol for secure API authentication.
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import re


# set up authentication

client_id = "bceacca66ac043b1a6d710f362b6d7b8"      # Replace with your Client ID
client_secret = "ad46077c60f440d3b4d890ad855f1ecd"  # Replace with your Client Secret

# Create a credentials manager

auth_manager = SpotifyClientCredentials(
    client_id = client_id,
    client_secret = client_secret
)

# Initailize Spotipy with auth

sp = spotipy.Spotify(auth_manager = auth_manager)  # sp - > Spotify API client

# Full track URL (Example - Time is Running out)
track_url = "https://open.spotify.com/track/1JSTJqkT5qHq8MDJnJbRE1"

# Extract track ID directly frlm URL  using regex
track_id = re.search(r'track/([a-zA-Z0-9]+)',track_url).group(1)

#Fetch track details 
track = sp.track(track_id)
print(track)

# Extract meatadata
track_data = {
    'Track Name' : track['name'],
    'Artist' : track['artists'][0]['name'], 
    'Album' : track['album']['name'],
    'Popularity': track['popularity'],
    'Duration (minutes)' : track['duration_ms'] / 60000 # convert to minutes

}

#Display metadata
print(f"\nTrack Name: {track_data['Track Name']}")
print(f"Artist: {track_data['Artist']}")
print(f"Album: {track_data['Album']}")
print(f"Popularity: {track_data['Popularity']}")
print(f"Duration: {track_data['Duration (minutes)']:.2f} minutes")

#convert metadat to Dataframe
df = pd.DataFrame([track_data])
print("\nTrack Data as DataFrame:")
print(df)

# Save metadata to csv 
df.to_csv('spotify_track_data.csv', index=False)

#visualize track data

features = ['Popularity','Duration (minutes)']
values = [track_data['Popularity'],track_data['Duration (minutes)']]

plt.figure(figsize=(8,5))
plt.bar(features, values, color = 'skyblue', edgecolor= 'black')
plt.title(f"Track Metadata  for '{track_data['Track Name']}'")
plt.ylabel('Value')
plt.show()




