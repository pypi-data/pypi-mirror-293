import speech_recognition as sr
import os
import webbrowser
import datetime
import pygame
from gtts import gTTS
import requests
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import re
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def get_name():
    if os.path.isfile("name.txt"):
        with open("name.txt","r") as f:
            name = f.read()
    else:
        say("Please say your name sir")
        name = takeCommand()
        if not("sorry" in name) :
            with open("name.txt","w") as f:
                f.write(name)
        else:
            name = takeCommand()
    return name
def get_google_description(query):
    search_url = f"https://www.google.com/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    description_header = soup.find('h3', class_='bNg8Rb OhScic zsYMMe BBwThe', string='Description')
    if description_header:

        description_span = description_header.find_next('span')

        if description_span:
            return description_span.get_text()

    return "Description not found."



def get_query(query,excluded_words):
    words = query.split(' ')
    pattern = re.compile(r'\b(?:' + '|'.join(excluded_words) + r')\b', re.IGNORECASE)
    words = [word for word in words if not pattern.search(word)]
    query = ' '.join(words)
    return query



def get_google_query(query):
    exclude_words=["google","search","on","in","about"]
    words = query.split(' ')
    pattern = re.compile(r'\b(?:' + '|'.join(exclude_words) + r')\b', re.IGNORECASE)
    words = [word for word in words if not pattern.search(word)]
    query = ' '.join(words)
    return query

def say(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    filename = "temp_audio.mp3"
    tts.save(filename)

    pygame.mixer.init()

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    os.remove(filename)

def search_youtube(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Search for the first occurrence of '/watch?v=' in the HTML content
    video_id_match = re.search(r'/watch\?v=([a-zA-Z0-9_-]+)', str(soup))
    if video_id_match:
        video_id = video_id_match.group(1)
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    return None

def spotify_play(text):
    excluded_words=["spotify","play","this","song","on","please","can","you"]
    song_name = get_query(text,excluded_words)
    song_name = song_name.replace(" ", "+")

    client_id = 'a2ffe956da264676adacbe37ca3b846d'
    client_secret = '0f1d0acde1e24d2690507d7161b9fff5'

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    results = sp.search(q=song_name, type='track', limit=10)

    if results['tracks']['items']:

        tracks = results['tracks']['items']
        tracks_sorted = sorted(tracks, key=lambda x: x['popularity'], reverse=True)

        most_popular_track = tracks_sorted[0]
        print(f"Track: {most_popular_track['name']}")
        print(f"Album: {most_popular_track['album']['name']}")
        track_url = most_popular_track['external_urls']['spotify']

        webbrowser.open(track_url)
    else:
        print("Song not found.")

def takeCommand(flag=1):
    if (flag == 0):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            # print("Listening...")
            audio = r.listen(source)
            try:
                print("Recognizing...")
                query = r.recognize_google(audio, language="en-IN")
                if ("start" in query):
                    print(f"User said: {query}")
                    return query
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                return "Sorry, I did not understand that."
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return "Sorry, there was an issue with the speech recognition service."
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        # print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-IN")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return "Sorry, I did not understand that."
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "Sorry, there was an issue with the speech recognition service."


def harmonyai():
    name=get_name()
    print('Welcome to HARMONY A.I')
    say(f" hi {name} how are you i am HARMONY A.I")
    while True:
        print("Listening...")
        query = takeCommand()

        if "open music" in query.lower():
            musicPath = "C:/Users/path/Downloads/song.mp3"
            os.system(f"start {musicPath}")  # Use 'start' for Windows

        # Check if the user wants to know the time
        elif "the time" in query.lower():
            now = datetime.datetime.now()
            time = now.strftime("%I:%M %p")
            say(f"{name}, the time is {time}")
        elif "date" in query.lower():
            date = datetime.date.today().strftime("%B %d, %Y")
            say(f"{name}, today's date is {date}")

        if "quit".lower() in query.lower():
            say(f"Goodbye, {name}")
            exit()

        elif "spotify".lower() in query.lower():
            spotify_play(query)
            say(f"Playing music for {name}")

        elif "youtube".lower() in query.lower():
            excluded_words = ["youtube", "on","in", "search","this","check","play"]
            content = get_query(query,excluded_words)
            videourl = search_youtube(content)
            if videourl:
                say(f"Searching for {content} on YouTube {name}")
                webbrowser.open(videourl)
            else:
                say(f"Something went wrong {name}.")

        elif "google".lower() in query.lower():
            search_query = get_google_query(query)
            say(f"Googling about {search_query}")
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(url)
            say(get_google_description(search_query))

        elif "unmute".lower() in query.lower() or "un mute".lower() in query.lower():
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(0, None)
            say(f"UnMuted volume {name}")


        elif "mute".lower() in query.lower():
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(1, None)


        elif "i love you".lower() in query.lower() or "i love u".lower() in query.lower() or "i like you".lower() in query.lower():
            say("Bro, as an AI model, I can't love. Go get a real girlfriend wastefellow.")
            with open("name.txt", 'a') as f:
                f.write("Brother")

        elif "stop listening".lower() in query.lower() or "shut up".lower() in query.lower():
            say(f"Okay {name}, waiting for your command.")
            while True:
                print("Waiting ...")
                query = takeCommand(0)
                print(f"Received query during while waiting")
                if "start".lower() in query.lower():
                    say(f"Starting, {name}.")
                    break
        elif "help".lower() in query.lower():
            say("To play music on spotify ")
            say("Say play song name on spotify")
            say(" To search on google")
            say("Say google about search query")
            say(" To search on youtube")
            say(" Say search topic name on youtube")
            say("To quit say harmony quit")
            say("To Mute the volume say mute the volume")
            say("To unmute the volume say unmute the volume")

        else:
            say("I'm not sure what you mean. Please try again.")