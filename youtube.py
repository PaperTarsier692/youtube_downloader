from pytube import YouTube
from pytube import Playlist
from pydub import AudioSegment
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import os
import inspect

total_bytes = 1

path = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))
    
def download_vid(link, path):
    print(f'Ladet das Video von "{YouTube(link).title}" herunter')
    yt_object = YouTube(link).streams.get_highest_resolution()
    try:
        yt_object.download(path)
    except:
        print('Oh Oh Fehler')

def download_aud(link, path):
    global total_bytes, current_video
    print(f'Ladet die Audio von "{YouTube(link).title}" herunter')
    yt_object = YouTube(link, on_progress_callback=progress, on_complete_callback=complete).streams.filter(only_audio = True).first()
    total_bytes = yt_object.filesize
    try:
        return yt_object.download(path)
    except:
        print('Oh Oh Fehler')
        

def convert_audio_format(input_file, output_format):
    audio = AudioSegment.from_file(input_file)
    output_file = input_file.rsplit('.', 1)[0] + '.' + output_format
    try:
        audio.export(output_file, format=output_format)
    except:
        print(f'Was soll das? Nicht unterstützes Format: {output_format}')


def setup():
    if not os.path.exists(f'{path}/videos/'):
        os.mkdir(f'{path}/videos/')
        print('Erstellt Ordner für die Videos')
        
    if not os.path.exists(f'{path}/audios/'):
        os.mkdir(f'{path}/audios/')
        print('Erstellt Ordner für die Audios')

def download_playlist(link, format):
    playlist = Playlist(link)

    video_urls = []
    video_urls = playlist.video_urls
    
    #for video in playlist.videos:
    #    video_urls.append(video.url)
    
    print(video_urls)
    
    counter = 0
    if 'video' in format:
        for url in video_urls:
            counter += 1
            download_vid(url, f"{path}/videos/")
            print(f'{counter}/{len(video_urls)} Videos heruntergeladen')
    counter = 0
    if 'audio' in format:
        for url in video_urls:
            counter += 1
            convert_audio_format(download_aud(url, f"{path}/audios/"), 'mp3')
            print(f'{counter}/{len(video_urls)} Audios heruntergeladen')

def progress(stream, chunk, bytes):
    global download_percent, total_bytes, progress_bar
    download_percent = 100 - (bytes / total_bytes * 100)
    progress_bar['value'] = download_percent

def complete(stream, path):
    print('Fertig')

def tkinter_setup():
    global progress_bar
    
    window = ThemedTk(theme="arc")
    window.title("Raubkopierer 3000")
    window.geometry("600x300")

    #style = ThemedTk(window)
    #style.theme_use('azure')  # Set the theme
    #style.configure('TFrame', background='blue')  # Set the background color
    #style.configure('TLabel', background='blue', foreground='white')  # Set the font color

    tab_control = ttk.Notebook(window)

    tab_playlist = ttk.Frame(tab_control)
    tab_control.add(tab_playlist, text="Playlist")
    label = tk.Label(tab_playlist, text="Link zur Playlist einfügen: ")
    label.grid(row=0, column=0)
    input_field = tk.Entry(tab_playlist, width=40)
    input_field.grid(row=0, column=1)
    selection_menu = ttk.Combobox(tab_playlist, values=['Video', 'Audio', 'Video & Audio'])
    selection_menu.grid(row=0, column=2)
    button = tk.Button(tab_playlist, text="Herunterladen", command=lambda: download_playlist(input_field.get(), selection_menu.get().lower()))
    progress_bar = ttk.Progressbar(tab_playlist, length=200, mode='determinate')
    label.grid(row=0, column=0)
    button.grid(row=1, column=0)
    progress_bar.grid(row=1, column=1)

    tab_video = ttk.Frame(tab_control)
    tab_control.add(tab_video, text="Video")
    label = tk.Label(tab_video, text="Link zum Video einfügen: ")
    label.grid(row=0, column=0)
#    input_field = tk.Entry(tab_video, width=50)
#    input_field.grid(row=0, column=1)

    tab_audio = ttk.Frame(tab_control)
    tab_control.add(tab_audio, text="Audio")
    label = tk.Label(tab_audio, text="Link zum Video einfügen: ")
    label.grid(row=0, column=0)
#    input_field = tk.Entry(tab_audio, width=50)
#    input_field.grid(row=0, column=1)

    tab_control.pack(expand=2, fill='both')
    window.mainloop()

setup()
tkinter_setup()
