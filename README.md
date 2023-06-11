# YtoS - YouTube to Spotify
<hr/>
YtoS is a simple program whose main purpose is to add your favourite YouTube song straight to the Spotify playlist.

## How does YtoS works
The operation of the program is simple and has two types of search.

- Automatic search (pasting YouTube url),
- Manual search (by typing song name and artist)

### Automatic search
By pasting YouTube link it scrape the web for video title and description. Then 
it starts searching in Spotify database by API for matching keywords. When it finds them it prompts and asks to search more. If
given title is right the next step is to add it to existing spotify playlist. It is also possible to create new playlist 
on the fly. When playlist with given name exists, program prompts with that information, if it's not, then it prompts 
with creating new one with given name. After this process the playlist name is stored for the next search, so you don't 
need to type the same playlist name over and over again. After all that program prompts to add song to playlist, this is
the last moment to decide if you want to add the song. Voilà, now your song is added with YouTube url to your spotify
playlist.

### Manual search
Manual searching differs from the previous one just in the first step by replacing the url pasting with typing in song 
name and artist. The next steps remain unchanged.

## How to start
First of all the spotify app must be created. For this purpose head to this 
[link](https://developer.spotify.com/documentation/web-api/concepts/apps)
and create new Spotify app for your account. Name your app and give it description of your choice. Then paste this: http://example.com
to "Redirect URIs" window. Next step is to copy "Client ID" and "Client Secret" by heading to "Settings"
in created app and paste those to file called **.env** that is located in main directory. 
**Remember not to share your Client Secret and Client ID! With this piece of blob cunning hacker can mess with your 
Spotify account!**. After that program is ready to use.

## How to run YtoS
YtoS comes with prebuilt virtual environment. To run program head to main directory and run PowerShell (right click ->
open in terminal). Then type: **"venv\Scripts\.\activate"**. Next step is to run **main.py** by typing **"python.exe main.py"**
For the first run, program will generate new file called **token.txt** with new token. In this case after running main.py
page will pop up in your browser. Copy URL of this page and paste it to terminal and hit enter. Now you can proceed and use.

This program is still in development.