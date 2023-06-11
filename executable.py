import spotipy
from spotipy.oauth2 import SpotifyOAuth
from youtubesearchpython import Video, ResultMode
import re
import os
from dotenv import load_dotenv
from pprint import pp

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPE = 'playlist-modify-public'
REDIRECT_URI = "http://example.com"


class Executable:

    def __init__(self):
        self.spotify_links = None
        self.latest_playlist = ""
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                            client_secret=CLIENT_SECRET,
                                                            redirect_uri=REDIRECT_URI,
                                                            scope=SCOPE, cache_path="token.txt"))
        self.user_id = self.sp.current_user()["id"]

    def creating_playlist(self):
        """Create new public playlist on Spotify"""

        playlist_name = input("Input name of the playlist (Case sensitive!): ")
        if playlist_name == "":
            playlist_name = self.latest_playlist
            print(f"Using latest playlist: {playlist_name}")
        self.latest_playlist = playlist_name
        playlist_exist = self.does_playlist_exist(playlist_name)
        if not playlist_exist:
            create = input(f"Do you want to create playlist called {playlist_name}? (y/n): ")
            if create == "y":
                playlist_id = self.sp.user_playlist_create(user=self.user_id,
                                                          name=playlist_name,
                                                          description="Adding songs from YouTube with YtoS extension.",
                                                          public=True)
                print(f"Creating playlist called: {playlist_name} with ID: {playlist_id['id']}")
                playlist_info = {
                    "playlist_id": playlist_id['id'],
                    "playlist_name": playlist_name,
                }
                return playlist_info
            else:
                return False
        else:
            print(f'Playlist already exist with name: {playlist_exist["playlist_name"]}')
            return playlist_exist

    # ------ Finding created playlist URI -----
    def does_playlist_exist(self, name):
        """Finds if playlist with given name exist on Spotify account"""

        for playlist in self.sp.current_user_playlists()["items"]:
            if playlist["name"] == name:
                playlist_info = {
                    "playlist_name": playlist["name"],
                    "playlist_id": playlist["id"],
                }
                return playlist_info
        return False

    def get_video_info(self, passed_url):
        """Function that gets links from YouTube video description."""

        video_info = Video.get(passed_url, mode=ResultMode.json, get_upload_date=True)
        video_info_json = {
            "title": video_info["title"],
            "description": video_info["description"],
            "channel": video_info["channel"],
            "keywords": video_info["keywords"],
        }
        return video_info_json

    def get_spotify_links(self, description):
        """This function search for artist links to Spotify. Links are stored as a list."""

        spotify_url_list = description["description"].splitlines()
        url_header = "https://open.spotify.com"
        self.spotify_links = [string for string in spotify_url_list if url_header in string]
        try:
            self.spotify_links[0]
        except IndexError:
            return False
        else:
            return self.spotify_links

    def get_artist_id(self, spotify_links):
        for name in spotify_links:
            try:
                artist_id = name.split("artist/", 1)[1]
                return artist_id
            except IndexError:
                pass

    def divide_title(self, title):
        """Function that strip and split given title. Returns list od elements."""

        split_title = re.split(r"[-()\/*|?.,]", title)
        strip_lspace = [string.lstrip() for string in split_title]
        strip_rspace = [string.rstrip() for string in strip_lspace]
        return strip_rspace

    def manual_spotify_searching(self, song_name, artist_name):
        """Function that allows to search manually Spotify database by passing song name and artist."""

        result = self.sp.search(q=f"track:{song_name}", type="track", limit=50)["tracks"]["items"]
        for position in result:
            # pp(f'artist name: {position["artists"][0]["name"]}')
            # pp(f'song name: {position["name"]}')
            artist_name_upper = artist_name.upper()
            if artist_name_upper in position["artists"][0]["name"].upper():
                spotify_song_info = {
                    "artist_id": position["artists"][0]["id"],
                    "artist_name": position["artists"][0]["name"],
                    "song_id": position["id"],
                    "song_name": position["name"],
                }
                print(f'\nSong found: {spotify_song_info["song_name"]} - {spotify_song_info["artist_name"]}')
                search = input("\nDo you want to continue searching? (y/n): ")
                if search == "y":
                    pass
                else:
                    return spotify_song_info
            # else:
            #     print(f"\n    Artist with name {artist_name} not found...")

    def search_on_spotify(self, song_name, artist_name):
        """Function that search for given song name and artist on Spotify database."""

        for song in song_name:
            result = self.sp.search(q=f"track:{song}", type="track", limit=50)["tracks"]["items"]
            for position in result:
                # pp(f'artist name: {position["artists"][0]["name"]}')
                # pp(f'song name: {position["name"]}')
                for artist in artist_name:
                    artist_name_upper = artist.upper()
                    if artist_name_upper in position["artists"][0]["name"].upper():
                        spotify_song_info = {
                            "artist_id": position["artists"][0]["id"],
                            "artist_name": position["artists"][0]["name"],
                            "song_id": position["id"],
                            "song_name": position["name"],
                        }
                        print(f'\nSong found: {spotify_song_info["song_name"]} - {spotify_song_info["artist_name"]}')
                        search = input("\nDo you want to continue searching? (y/n): ")
                        if search == "y":
                            pass
                        else:
                            return spotify_song_info
                    # else:
                    #     print(f"\n    Artist with name {artist} not found...")
        return False

    def add_song(self, song_data, playlist_data):
        """Function that adds available songs to the playlist"""
        track = [song_data["song_id"]]
        what_to_do = input(f'\nDo you want to add song to "{playlist_data["playlist_name"]}"? (y/n): ')
        if what_to_do == "y":
            self.sp.playlist_add_items(playlist_id=playlist_data["playlist_id"], items=track)
            print("\nSong successfully added!\n")
        else:
            print("\nProcess aborted.\n")
