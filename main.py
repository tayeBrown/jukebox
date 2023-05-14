import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import json

def create_spotify():
    with open("config.json") as config:
        data = json.load(config)
    
    auth_manager = SpotifyOAuth(
        scope=data["SCOPE"],
        username=data["USERNAME"],
        redirect_uri=data["USERNAME"],
        client_id=data["CLIENT_ID"],
        client_secret=data["CLIENT_SECRET"])

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    return auth_manager, spotify

def refresh_spotify(auth_manager, spotify):
    token_info = auth_manager.cache_handler.get_cached_token()
    print(token_info)
    if auth_manager.is_token_expired(token_info):
        print("Fetching new token")
        auth_manager, spotify = create_spotify()
    return auth_manager, spotify

def select_playlist():
    p_list = get_user_playlists()
    for index, i in enumerate(p_list):
        name = i["name"]
        print(f"{index}, {name}")
    current_playlist_index = input("Please select a number to choose a playlist")
    return p_list[int(current_playlist_index)]

def get_user_playlists():
    playlists = spotify.current_user_playlists()["items"]
    return playlists

def get_current_track():
    playing = spotify.currently_playing()
    if playing:
        print(playing["item"]["name"])
    else:
        print("Nothing is playing. Please select a track")

if __name__ == '__main__':
    auth_manager, spotify = create_spotify()

    while True:
        auth_manager, spotify = refresh_spotify(auth_manager, spotify)
        get_current_track()
        # Need to implement a menu selection here.
        # select_playlist()
        time.sleep(60)