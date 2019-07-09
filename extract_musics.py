import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://www.vagalume.com.br/'

# Given a music, this function returns its lytics
def get_lyrics(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    lyrics = soup.find(id='lyrics')
    return str(lyrics).replace('<br/>', '\n').replace('<div id="lyrics">', '').replace('</div>', '')

# Given an artist, this function returns all songs of this artist
def get_music_names(artist):
    url_artist = url + '/{}/'.format(artist)
    req = requests.get(url_artist)
    soup = BeautifulSoup(req.content, 'html.parser')
    musics = soup.findAll("a", {'class':'nameMusic'})

    music_names = []
    for line in musics:
        music_names.append(line.get('href'))
    return music_names

# Get top 100 artists in vagalume website
def get_top_100():
    url_top = url + 'top100/artistas/nacional/'
    req = requests.get(url_top)
    soup = BeautifulSoup(req.content, 'html.parser')
    top_100 = soup.findAll('a', {'class': 'w1 h22'})
    for i in range(len(top_100)):
        top_100[i] = top_100[i].get('href')
    
    return top_100

# Testing funtctions above:


top_100 = get_top_100()

final_list = []

for artist in top_100:
    music_names = get_music_names(artist)
    for music in music_names:
        lyrics = get_lyrics(url + music)
        final_list.append([artist, music, lyrics])

df = pd.DataFrame(final_list, columns=['artist', 'music_name', 'lyrics'])
df.to_csv('data/dataset_lyrics.csv', index=False) 

