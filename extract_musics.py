import pandas as pd
import requests
from bs4 import BeautifulSoup

# Given a music, this function returns its lytics
def get_lyrics(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    lyrics = soup.find(id='lyrics')
    return str(lyrics).replace('<br/>', '\n').replace('<div id="lyrics">', '').replace('</div>', '')

# Given an artist, this function returns all songs of this artist
def get_music_names(artist):
    url_artist = url + '/{}/'.format(artist.replace(' ','-'))
    req = requests.get(url_artist)
    soup = BeautifulSoup(req.content, 'html.parser')
    musics = soup.findAll("a", {'class':'nameMusic'})

    music_names = []
    for line in musics:
        music_names.append(line.get('href'))
    return music_names

# Testing functions above:

url = 'https://www.vagalume.com.br/'

music_names = get_music_names('the calling')

for music in music_names:
    print(get_lyrics(url + music))
    print('-------------------------------------------------')
