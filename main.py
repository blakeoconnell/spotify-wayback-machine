from pprint import pprint
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import auth

BILLBOARD_URL = auth.BILLBOARD_URL
SPOTIFY_CLIENT_ID = auth.SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = auth.SPOTIFY_CLIENT_SECRET
SPOTIFY_REDIRECT_URI = auth.SPOTIFY_REDIRECT_URI
SPOTIFY_SCOPE = auth.SPOTIFY_SCOPE

user_date = input("Which year would you like to travel to? Type the date in this format YYYY-MM-DD: ")
year = user_date[0:4]

response = requests.get(f"{BILLBOARD_URL}/{user_date}")

html = response.text

soup = BeautifulSoup(html, "html.parser")

song_list = soup.find_all(name="span", class_="chart-element__information__song")

song_names = [item.getText() for item in song_list]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope=SPOTIFY_SCOPE))
current_user_id = sp.current_user()["id"]

song_URIs = []
for song in song_names:
    query = f"track:{song} year:{year}"
    try:
        song_URIs.append(sp.search(q=query, type="track")["tracks"]["items"][0]["uri"])
    except IndexError:
        print("Song not available on Spotify. Moving on...")


playlist_id = sp.user_playlist_create(current_user_id, f"{user_date} Billboard 100", public=False)["id"]
sp.playlist_add_items(playlist_id, song_URIs)
