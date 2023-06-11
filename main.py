from executable import Executable
from pprint import pp

account = Executable()


# ----- Automatic searching -----
def automatic_searching(url):
    video_info = account.get_video_info(url)
    divided_title = account.divide_title(video_info["title"])
    song_info = account.search_on_spotify(song_name=divided_title, artist_name=video_info["keywords"])
    if not song_info:
        return print("Song not found with automatic searching.\n")
    playlist_info = account.creating_playlist()
    if not playlist_info:
        return print("Creating new playlist aborted.\n")
    account.add_song(song_data=song_info, playlist_data=playlist_info)


# ----- Manual searching -----
def manual_searching(song_name, artist):
    song_info = account.manual_spotify_searching(song_name, artist)
    if not song_info:
        return print("Song not found with manual searching.\n")
    playlist_info = account.creating_playlist()
    if not playlist_info:
        return print("Creating new playlist aborted.\n")
    account.add_song(song_data=song_info, playlist_data=playlist_info)


def main_loop():
    what_to_do = input("Do you want to search automatically with passing URL or manually "
                       "by passing song name and author? (a/m): ")
    if what_to_do == "a":
        url = input("Please input YouTube URL: ")
        automatic_searching(url)
    elif what_to_do == "m":
        song_name = input("Please input song name: ").rstrip()
        artist = input("Please input artist: ").rstrip()
        manual_searching(song_name, artist)
    else:
        print("\nWrong input. Process aborted.")
        return True
    return

# account.does_playlist_exist("test")
loop = False
while not loop:
    loop = main_loop()
