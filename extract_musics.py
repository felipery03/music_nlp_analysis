import pandas as pd
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob as tb #pip install textblob
import nltk




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

# Get top 20 music of given artist from Letras.mus.br
def get_letras_top20_musics(artista):
    htmlparse = BeautifulSoup(requests.get("https://www.letras.mus.br/"+artista.replace(' ', '-')).content, 'html.parser')
    testes = htmlparse.find('div', {'class':'artista-top g-sp g-pr'})
    music = testes.findAll('span')
    return music

# translate phrase words to pt 
def get_pt(frase, vizinhanca):
    fraseretorno = ""
    split_frase = frase.split(" ")
    for x in range (0, len(split_frase)):
        palavra = split_frase[x]
        if(len(palavra)>2):                 #function only works for words with len>2
            if(check_isLanguage(palavra)):      #checks if word and phrase are same language
                fraseretorno+=palavra
            else:                           #not same language
                fraseretorno+=getFinalword(split_frase,x,vizinhanca)
        else:
            fraseretorno+=palavra
        fraseretorno+=" "
    return fraseretorno

def check_isLanguage(palavra):
    palavratb = tb(palavra)
    lang_palavra = palavratb.detect_language()
    if(lang_palavra != "pt"):
        return False
    return True

def getFinalword(vetor_frase, palavra_position, neighborhood_size):       #check with neighborhood and gives final word
    menor, maior = calculo_neighborhood(vetor_frase,palavra_position, neighborhood_size)
    frasefinal = ""
    for i in range (menor, maior+1):
        frasefinal+= " " + vetor_frase[palavra_position+i]            
    frasefinaltb = tb(frasefinal)
    lang_frasefinal = frasefinaltb.detect_language()
    if(lang_frasefinal != "pt"):
        palavratb = tb(vetor_frase[palavra_position])
        return str(palavratb.translate(to="pt"))
    return vetor_frase[palavra_position]    

def calculo_neighborhood(vetor_frase, palavra_position,neighborhood_size):
    menor = 0
    for i in range (neighborhood_size,0,-1):                    
        if palavra_position-i >= 0:
            menor = -i                        
            break
    maior = 0
    for i in range (neighborhood_size,0,-1):
        if palavra_position+i < len(vetor_frase):
            maior = i
            break
    return menor, maior
            


# Testing funtctions above:


# top_100 = get_top_100()

# final_list = []

# for artist in top_100:
#    music_names = get_music_names(artist)
#    for music in music_names:
#        lyrics = get_lyrics(url + music)
#        final_list.append([artist, music, lyrics])

# df = pd.DataFrame(final_list, columns=['artist', 'music_name', 'lyrics'])
# df.to_csv('data/dataset_lyrics.csv', index=False) 

# top20music = get_letras_top20_musics("lady gaga")
# for m in top20music:
#    print(m.text)

print(get_pt("eu perguntava do you wanna dance?",1))
print(get_pt("juntos e shallow now",1))