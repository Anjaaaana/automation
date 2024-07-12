import time
import sys
import os
from pytube import YouTube
import pygame
from youtubesearchpython import VideosSearch

class Song:
    def __init__(self, title, artist, duration):
        self.title = title
        self.artist = artist
        self.duration = duration

class Node:
    def __init__(self, song, prev=None, next=None):
        self.song = song
        self.prev = prev
        self.next = next

def add_song(start, title, artist, duration):
    new_song = Song(title, artist, duration)
    new_node = Node(new_song)
    if start:
        new_node.prev = start.prev
        new_node.next = start
        start.prev.next = new_node
        start.prev = new_node
        return start
    else:
        new_node.next = new_node
        new_node.prev = new_node
        return new_node

def remove_song(start, del_song_title):
    if start.next == start and start.song.title == del_song_title:
        return None
    else:
        if start.song.title == del_song_title:
            start.prev.next = start.next
            start.next.prev = start.prev
            return start.next
        else:
            temp = start
            while True:
                if temp.song.title == del_song_title:
                    temp.prev.next = temp.next
                    temp.next.prev = temp.prev
                    return start
                if temp == start:
                    print(f"\n>>Error: Song '{del_song_title}' not found.")
                    return start
                temp = temp.next

def play_song(start, current_song):
    if start:
        print(f"\n>> Now Playing: '{current_song.song.title}' by {current_song.song.artist}")
        play_audio(current_song)
    else:
        print("Playlist is empty!")

def play_audio(current_song):
    pygame.mixer.init()

    # Specify the folder path for the audio file
    folder_path = 'audio_files'

    # Check if the folder exists
    if os.path.exists(folder_path):
        mp3_file = f"{current_song.song.title}.mp3"
        file_path = os.path.join(folder_path, mp3_file)

        pygame.mixer.music.load(file_path.encode('utf-8'))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        print(f"Error: Folder '{folder_path}' not found.")

def prev_song(start, current_song):
    if start:
        print(f"\n>> Skipping to the previous song: {current_song.prev.song.title}!")
        return start, current_song.prev
    else:
        print("No song to skip!")
        return None, None

def next_song(start, current_song):
    if start:
        print(f"\n>> Skipping to the next song: {current_song.next.song.title}!")
        return start, current_song.next
    else:
        print("No song to skip!")
        return None, None

def show_playlist(start):
    current = start
    while current:
        print(f"SONG NAME: {current.song.title}")
        print(f"ARTIST: {current.song.artist}")
        print(f"DURATION: {current.song.duration}\n")
        current = current.next
        if current == start:
            break

def search_and_download(query, start):
    try:
        # Use youtube-search-python to search for the video
        video_search = VideosSearch(query, limit=1).result()

        if video_search['result']:
            video_url = f"https://www.youtube.com/watch?v={video_search['result'][0]['id']}"
            # Extract information from the video
            yt = YouTube(video_url)
            title = yt.title
            artist = yt.author
            duration = time.strftime('%M:%S', time.gmtime(yt.length))

            # Add the song to the playlist
            start = add_song(start, title, artist, duration)

            # Specify the full path for downloading the audio file
            file_path = os.path.join('audio_files', f"{title}.mp3")

            # Download the audio
            yt.streams.filter(only_audio=True).first().download(output_path=file_path)

            print(f"\n>> Song '{title}' downloaded and added to the playlist.")
        else:
            print(f"\n>> Error: No search results found for '{query}'.")
    except Exception as e:
        print(f"\n>> Error: {str(e)}")

def menu(start, current_song):
    print("\n---------------------------------------------------")
    print("Welcome to my Song Player!\n")
    print("Please select an action --> [1/2/3/4/5/6/7/8/99]\n")
    print("1. Play Song \t\t[1]")
    print("2. Add Song \t\t[2]")
    print("3. Previous Song \t[3]")
    print("4. Next Song \t\t[4]")
    print("5. Delete Song \t\t[5]")
    print("6. Show Playlist \t[6]")
    print("7. Search & Download \t[7]")
    print("8. Exit \t\t[8]")
    print("99. Clear Screen\t[99]\n")

    try:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            play_song(start, current_song)
        elif choice == 2:
            song_title = input("\nEnter Song Title: ").title()
            song_artist = input("Enter Song Artist: ").title()
            song_duration = input("Enter Song Duration (0:00): ")
            start = add_song(start, song_title, song_artist, song_duration)
            print("\n---------------------------")
            print(f"Song '{song_title}' added successfully!")
            print("---------------------------\n\n")
        elif choice == 3:
            start, current_song = prev_song(start, current_song)
        elif choice == 4:
            start, current_song = next_song(start, current_song)
        elif choice == 5:
            title = input("Enter the song title to delete: ").title()
            start = remove_song(start, title)
        elif choice == 6:
            print("\n---------------------------")
            print("\tYour Playlist")
            print("---------------------------")
            show_playlist(start)
            print("---------------------------\n\n")
            time.sleep(1)
        elif choice == 7:
            query = input("\nEnter song name to search and download: ")
            search_and_download(query, start)
        elif choice == 8:
            print("Exiting. . .")
            time.sleep(1)
            pygame.quit()
            sys.exit()
        elif choice == 99:
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
        else:
            raise ValueError("Please enter a valid input [1/2/3/4/5/6/7/8/99]")

    except Exception as err:
        print(f"\nSomething unexpected occurred: {str(err)}\n")

    return start, current_song

if __name__ == "__main__":
    start = None
    current_song = None

    pygame.init()

    while True:
        start, current_song = menu(start, current_song)
