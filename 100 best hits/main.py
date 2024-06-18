from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import os
from dotenv import load_dotenv

load_dotenv()

ID = os.getenv("CLIENT_ID")
SECRET = os.getenv("CLIENT_SECRET")

date = input("What year would you want to go back to?Type in this format YYYY-MM-DAY: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
data = response.text

soup = BeautifulSoup(data, "html.parser")

songs = [song.getText().replace('\t', '').replace('\n', '') for song in soup.select("li  h3")]
song_urls = []

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id = ID,
        client_secret = SECRET,
        redirect_uri = "http://example.com",
        scope="playlist-modify-private",
        cache_path = "token.txt",
        show_dialog=True,
    )
)

user_id = sp.current_user()["id"]
year = date.split("-")[0]

for song in songs:
    answers = sp.search(q=f"track:{song}, year:{year}", type="track")
    try:
        result = answers["tracks"]["items"][0]["uri"]
        song_urls.append(result)
        print(song_urls)
    except IndexError:
        print(f"{song} not found in the spotify library")

for song in songs:
    answers = sp.search(q=f"track:{song}, year:{year}", type="track")
    print(answers)

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_urls)
