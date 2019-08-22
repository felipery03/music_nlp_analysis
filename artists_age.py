import datetime
import requests
import json
import os

url = 'https://www.vagalume.com.br'
ages_addr = 'ages.txt'
topUp = ['racionais-mcs', 'emicida', 'hungria', 'projota', 'tribo-da-periferia', 'chico-buarque', 'tiao-carreiro-e-pardinho', 'kamaitachi', 'caetano-veloso', 'legiao-urbana']
topDown = ['midian-lima', 'raca-negra', 'fernandinho', 'gabriela-rocha', 'andre-valadao', 'padre-marcelo-rossi', 'diante-do-trono', 'aline-barros', 'eyshila', 'ze-neto-e-cristiano']
ages = {}

def get_year(items):
	for x in range(0, len(items)-1):
		print(x)
		if int(items[len(items)-1-x]['year'], 10) > 0:
			return int(items[len(items)-1-x]['year'], 10)

def get_age(artist):
	url_artist = url + '/{}/index.js'.format(artist)
	req = requests.get(url_artist)
	albumAge = get_year(json.loads(req.content)['artist']['albums']['item'])
	if albumAge != None:
		estimateAge = datetime.datetime.now().year - albumAge
		ages[artist] = str(estimateAge)
		add_age(ages_addr, artist)

def add_age(arquivo, chave):
    if os.path.exists(arquivo):
        f = open(arquivo,'a', encoding='utf-8')
    else:
        f = open(arquivo, 'w+',encoding='utf-8')
    f.write(chave +":"+ ages[chave]+"\n")
    f.close()

for x in topUp:
	get_age(x)

for y in topDown:
	get_age(y)