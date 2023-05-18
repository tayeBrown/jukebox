import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import json

class Player:

    def __init__(self):
        # TODO set default playlist here
        self.active_device_id = None
        self.playlist_id = None
        self.user_id = None

    def create_spotify(self):
        with open("config.json") as config:
            data = json.load(config)
        
        auth_manager = SpotifyOAuth(
            scope=data["SCOPE"],
            username=data["USERNAME"],
            redirect_uri=data["REDIRECT"],
            client_id=data["CLIENT_ID"],
            client_secret=data["CLIENT_SECRET"])

        spotify = spotipy.Spotify(auth_manager=auth_manager)
        self.playlist_id = data["DEFAULT_PLAYLIST"]
        self.user_id = data["USER_ID"]

        return auth_manager, spotify
    
    def get_devices(self):
        """"
            Get the ID of a currently active device for the signed in user
            Returns the device ID
        """
        device_list = spotify.devices()
        print("Getting Devices...")
        for i in device_list["devices"]:
            if i["is_active"]:
                return i["id"]


    def refresh_spotify(self, auth_manager, spotify):
        """
            Checks for an existing auth token
            If one does not exist, creates a new token
            Else if the current token is expired, creates a new token
        """
        token_info = auth_manager.cache_handler.get_cached_token()
        print(token_info)
        if token_info == None:
            print("Fetching new token")
            auth_manager, spotify = self.create_spotify()
        elif auth_manager.is_token_expired(token_info):
            print("Fetching new token")
            auth_manager, spotify = self.create_spotify()
        return auth_manager, spotify

    def select_playlist(self):
        """
            Selects a playlist to set as the global playlist
            This playlist is used to select and queue tracks from
        """
        p_list = self.get_all_playlists()
        for index, i in enumerate(p_list):
            name = i["name"]
            print(f"{index}, {name}")
        current_playlist_index = input("Please select a number to choose a playlist")
        print("Playlist selected: " + str(p_list[int(current_playlist_index)]["name"]))
        self.playlist_id = str(p_list[int(current_playlist_index)]["id"])
        

    def setup_playlist(self):
        """
            When passed playlist information, gets all the songs from that playlist
            Displays the songs as a selectable menu
        """
        print("IMPLEMENT ME")

    def get_user_playlists(self):
        """
            Gets all the playlists associated with a user
            Returns the list of playlists
            Currently not used
        """
        playlists = spotify.current_user_playlists()["items"]
        return playlists
    

    def get_all_playlists(self):
        """
            Gets all the playlists associated with a user
            This differs from get_user_playlists because it includes the playlists
            that the user did not make themselves
        """
        playlists = spotify.user_playlists(self.user_id)["items"]
        # for i in playlists:
        #     print(i["name"] + ": " + i["id"])
        return playlists


    def get_current_track(self):
        """
            Mostly a test function
            Checks if a track is playing. If so, prints the name of the track.
            If not, asks the user to select a track.
        """
        playing = spotify.currently_playing()
        if playing:
            print(playing["item"]["name"])
        else:
            print("Nothing is playing. Please select a track")
            self.get_track_list()
    
    def get_track_list(self):
        """
            Uses the current playlist (self.playlist_id) to get a full list of tracks
            Adds the track name and track id to a list of tracks TODO check if track name will 
                ever be useful to keep here
            Returns the list
        """
        print("GET TRACK LIST")
        print(self.playlist_id)
        track_list = spotify.playlist_tracks(self.playlist_id)
        items = track_list["items"]
        tracks = []
        for i, t in enumerate(items):
            track = items[i]["track"]
            track_ids = [track["name"], track["id"]]
            tracks.append(track_ids)
        return tracks

    def select_song(self):
        tracks = self.get_track_list()
        print("Please select a track: ")
        for index, i in enumerate(tracks):
            print(str(index) + ": " + i[0])
        track_choice = input("Awaiting track input...")
        if track_choice.isdigit():
            # Choose the track ID from the [track_name, track_id] sublist inside tracks list
            #uri = list(f"spotify:track:{tracks[int(track_choice)][1]}")
            t = tracks[int(track_choice)][1]
            uri = [f"spotify:track:{t}"]
            print(uri)
            spotify.start_playback(uris=uri)

    def add_song_to_queue(self):
        print("IMPLEMENT ME")
        # Reminder for tomorrow: add_to_queue(uri, device_id=None) is the method I want here.
        # Otherwise, will do pretty much the same as select_song()
        # So will queue() no doubt
        tracks = self.get_track_list()
        print("Please select a track: ")
        for index, i in enumerate(tracks):
            print(str(index) + ": " + i[0])
        track_choice = input("Awaiting track input...")
        if track_choice.isdigit():
            # Choose the track ID from the [track_name, track_id] sublist inside tracks list
            t = tracks[int(track_choice)][1]
            print(t)
            uri = f"spotify:track:{t}"
            print(uri)
            spotify.add_to_queue(uri)

    def pause():
        print("IMPLEMENT ME")
        # pause_playback(device_id=None)
        # Will be needed for button controls later
    
    def next_track():
        print("IMPLEMENT ME")
        # next_track(device_id=None)
        #  Will be needed for button controls later
    
    def previous_track():
        print("IMPLEMENT ME")
        # previous_track(device_id=None)
        # Will be needed for button controls later

class Menu: 
    def menu_builder(self, player):
        """
            Users can select a playlist
            Users can play a track from the current playlist
            Users can add a track to the current queue
        """
        menu = ["Placeholder", "1. Select a playlist", "2. Play a new track", "3. Add song to queue"]
        for index, i in enumerate(menu):
            if index != 0:
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
        # TODO there has to be a better way of doing this than just
        # infinite looping
        # its actually getting really annoying
        auth_manager, spotify = player.refresh_spotify(auth_manager, spotify)
        menu = Menu()
        menu.menu_builder(player)
        #player.get_all_playlists()
        # Need to implement a menu selection here.
        # select_playlist()
        #player.get_devices()