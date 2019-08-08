# -*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob as tb #pip install textblob
import nltk
import langid
import os




url = 'https://www.vagalume.com.br/'

langid.set_languages(['pt','es','en'])

dicionario_addr = 'dicionario.txt'
dicionario = {}

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

# Given an artist, this function returns 25 top songs of this artist
def get_top25_music_names(artist):
    print("Artista: " + artist)
    url_artist = url + '/{}/'.format(artist)
    req = BeautifulSoup(requests.get(url_artist).content, 'html.parser')
    trecho = req.find('ol', {'id': 'topMusicList'})
    if(trecho != None):
        musicas = trecho.findAll('a', {'class': 'nameMusic'})
        musicaddr = []
        for mus in musicas:
            musicaddr.append(mus.get('href'))
        print (musicaddr)
        return musicaddr
    else:
        return get_music_names(artist)

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
# avoid due to excedent use of google requisitions (limited to 1000/day)
# def get_pt(frase, vizinhanca):
#     fraseretorno = ""
#     split_frase = frase.split(" ")
#     for x in range (0, len(split_frase)):
#         palavra = split_frase[x]
#         if(len(palavra)>2):                 #function only works for words with len>2
#             if(check_isLanguage(palavra)):      #checks if word and phrase are same language
#                 fraseretorno+=palavra
#             else:                           #not same language
#                 fraseretorno+=getFinalword(split_frase,x,vizinhanca)
#         else:
#             fraseretorno+=palavra
#         fraseretorno+=" "
#     return fraseretorno

# def check_isLanguage(palavra):
#     palavratb = tb(palavra)
#     lang_palavra = palavratb.detect_language()
#     if(lang_palavra != "pt"):
#         return False
#     return True

# def getFinalword(vetor_frase, palavra_position, neighborhood_size):       #check with neighborhood and gives final word
#     menor, maior = calculo_neighborhood(vetor_frase,palavra_position, neighborhood_size)
#     frasefinal = ""
#     for i in range (menor, maior+1):
#         frasefinal+= " " + vetor_frase[palavra_position+i]
#     frasefinaltb = tb(frasefinal)
#     lang_frasefinal = frasefinaltb.detect_language()
#     if(lang_frasefinal != "pt"):
#         palavratb = tb(vetor_frase[palavra_position])
#         return str(palavratb.translate(to="pt"))
#     return vetor_frase[palavra_position]

    # translate phrase words to pt
def langid_pt(frase_init, vizinhanca):
    frase = frase_init.lower()
    fraseretorno = ""
    split_frase = frase.split(" ")
    for x in range (0, len(split_frase)):
        palavra = split_frase[x].rstrip().lstrip()
        if(langid_ispt(palavra)):      #checks if word and phrase are same language
            print("não vai traduzir " + palavra)
            fraseretorno+=palavra
        else:                           #not same language
            print("vai traduzir " +palavra)
            fraseretorno+=langid_translate(split_frase,x,vizinhanca)
        fraseretorno+=" "
    print(fraseretorno)
    return fraseretorno

def langid_ispt(palavra):
    lang = langid.classify(palavra) #devolve formato (lingua, confiança)
    if(lang[0] !="pt"):
        return False
    return True

def langid_translate(vetor_frase, palavra_position, neighborhood_size):       #check with neighborhood and gives final word
    menor, maior = calculo_neighborhood(vetor_frase,palavra_position, neighborhood_size)
    frasefinal = ""
    for i in range (menor, maior+1):
        frasefinal+= vetor_frase[palavra_position+i]
        if(i!=maior):
            frasefinal+=" "
    lang_frasefinal = langid.classify(frasefinal)
    #print("ling: "+lang_frasefinal[0])
    if(lang_frasefinal[0] == "pt"):
        return vetor_frase[palavra_position]
    else:
        try:
            return pt_dictionary(vetor_frase[palavra_position], lang_frasefinal[0]).rstrip().lstrip()
        except:
            return vetor_frase[palavra_position]


def pt_dictionary(palavra, lang):
    if palavra in dicionario:
        print(palavra + ": já está no dic!")
        return dicionario[palavra]
    else:
        palavratb = tb(palavra)
        print("traduzir para colocar no dic " + palavra)
        traducao = str(palavratb.translate(from_lang=lang,to="pt"))
        print("traduzido " + palavra + " para " + traducao)
        dicionario[palavra] = traducao
        add_dicionario(dicionario_addr,palavra)
        print(palavra + ": adicionado ao dic!")
        return traducao

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

def load_dicionario(arquivo):
    if os.path.exists(arquivo):
        fl = open(arquivo, "r", encoding='utf-8')
        for line in fl.readlines():
            palavra, traducao = line.split(':')
            dicionario[palavra] = traducao
        fl.close()
    else:
        fl = open(arquivo, 'w+')

def add_dicionario(arquivo, chave):
    if os.path.exists(arquivo):
        f = open(arquivo,'a', encoding='utf-8')
    else:
        f = open(arquivo, 'w+',encoding='utf-8')
    f.write(chave +":"+ dicionario[chave]+"\n")
    f.close()

def translate(song):
    verses = song.split('\n')
    translated_verses = list(map(lambda x: langid_pt(x,1), verses))
    full_song = "".join(translated_verses)
    print(full_song)
    return full_song

# Testing funtctions above:


# top_100 = get_top_100()

# final_list = []

# for artist in top_100:
# #   music_names = get_music_names(artist)
#     music_names = get_top25_music_names(artist)
#     for music in music_names:
#         lyrics = get_lyrics(url + music)
#         final_list.append([artist, music, lyrics])

# df = pd.DataFrame(final_list, columns=['artist', 'music_name', 'lyrics'])
# df.to_csv('data/dataset_lyrics.csv', index=False)

#Teste da função para usar menos requisições!
#teste do dicionario


load_dicionario(dicionario_addr)

import re

df = pd.read_csv('data/dataset_lyrics.csv')

#removes compilations
df = df[(df.artist != '/colecao-amo-voce/')&(df.artist != '/corinhos-infantis/')&(df.artist != '/corinhos-evangelicos/')&
        (df.artist != '/harpa-crista/')&(df.artist != '/hinos/')&(df.artist != '/musicas-catolicas/')&(df.artist != '/musicas-gospel/')&
        (df.artist != '/pineapple/')&(df.artist != '/umbanda/')&(df.artist != '/alok/')]

#removes artists with less than 25 songs
df = df[(df.artist != '/melim/')&(df.artist != '/kell-smith/')&(df.artist != '/midiam-lima/')&(df.artist != '/isadora-pompeo/')]

#data cleansing
df['lyrics'] = df['lyrics'].str.strip('<div data-plugin=""googleTranslate"" id=""lyrics"">')
df['lyrics'] = df['lyrics'].str.strip('<img alt="Instrumental" class="instrumental-icon" src="/img/etc/instrumental.png"/')
df['lyrics'] = df['lyrics'].apply(lambda x: x.lower())
df['lyrics'] = df['lyrics'].apply(lambda x: re.sub('[0-9!,.;:\]?}{()"["|@#$%*]', "", x))

# df['translated'] = df['lyrics'].apply(lambda x: translate(x))

# df.to_csv('data/dataset.csv', index=False)

palavratb = tb("morning")
trad = str(palavratb.translate(from_lang="en",to="pt"))
print(trad)


# print("Dicionario inicial: ")
# for d in dicionario:
#     print("- " + d + " : " + dicionario[d])
# print("\n\n fim \n\n")
# a = langid_pt("você wanna dance?",0)
# # langid_pt("gusta",0)
# # langid_pt("hello",0)
# # langid_pt("Hello",0)
# print("Dicionario final: ")
# for d in dicionario:
#     print("- " + d + " : " + dicionario[d])
# print("\n\n fim \n\n")
# print(a)




#print(get_top25_music_names('marilia-mendonca'))

# top20music = get_letras_top20_musics("lady gaga")
# for m in top20music:
#    print(m.text)

# print(get_pt("eu perguntava do you wanna dance?",1))
# print(get_pt("juntos e shallow now",1))
