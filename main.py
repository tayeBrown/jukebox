import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import json

class Player:

    def __init__(self):
        # TODO set default playlist here
        self.playlist = None

    def create_spotify(self):
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

    def refresh_spotify(self, auth_manager, spotify):
        token_info = auth_manager.cache_handler.get_cached_token()
        print(token_info)
        if auth_manager.is_token_expired(token_info):
            print("Fetching new token")
            auth_manager, spotify = self.create_spotify()
        return auth_manager, spotify

    def select_playlist(self):
        p_list = self.get_user_playlists()
        for index, i in enumerate(p_list):
            name = i["name"]
            print(f"{index}, {name}")
        current_playlist_index = input("Please select a number to choose a playlist")
        print("Playlist selected: " + str(p_list[int(current_playlist_index)]["name"]))
        

    def setup_playlist(self, playlist: int):
        """
            When passed playlist information, gets all the songs from that playlist
            Displays the songs as a selectable menu
        """
        print("IMPLEMENT ME")

    def get_user_playlists(self):
        playlists = spotify.current_user_playlists()["items"]
        return playlists

    def get_current_track(self):
        playing = spotify.currently_playing()
        if playing:
            print(playing["item"]["name"])
        else:
            print("Nothing is playing. Please select a track")

    def select_song(self):
        print("IMPLEMENT ME")

    def add_song_to_queue(self):
        print("IMPLEMENT ME")

class Menu: 
    def menu_builder(self, player):
        """
            Users can select a playlist
            Users can play a track from the current playlist
            Users can add a track to the current queue
        """
        menu = ["Placeholder", "1. Select a playlist", "2. Play a new track", "3. Add song to queue"]
        for index, i in enumerate(menu):
            if index is not 0:
                print(i)
        choice = input("What would you like to do?")
        try:
            choice = int(choice)
        except ValueError:
            print("Valid numbers only!")
        if choice == 1:
            print("Selecting new playlist...")
            player.select_playlist()
        elif choice == 2:
            print("Please choose a new song...this will start  playing immediately")
            player.select_song()
        elif choice == 3:
            print("Select a song to add to the current queue")
            player.add_song_to_queue()



if __name__ == '__main__':
    player = Player()
    auth_manager, spotify = player.create_spotify()

    while True:
        auth_manager, spotify = player.refresh_spotify(auth_manager, spotify)
        menu = Menu()
        menu.menu_builder(player)
        player.get_current_track()
        # Need to implement a menu selection here.
        # select_playlist()
        time.sleep(60)