import pandas
import time
import google_play_scraper as gps
from datetime import datetime
from dateutil.parser import parse
from nltk import word_tokenize, corpus, stem, download
import unicodedata
import re
import UpdateOrCreateFile

app_id = 'br.gov.meugovbr'

def joinTokens(tokens):    
	string = ""
	for i in tokens:
		string += (i + " ")
	return string 

def removeSpecialCharacters(old_string):
	nfkd = unicodedata.normalize('NFKD', old_string)
	new_string = u"".join([c for c in nfkd if not unicodedata.combining(c)])
	new_string = new_string.lower()
	return re.sub('[^a-zA-Z0-9 \\\]', '', new_string)    


def buscaString(comentarios, frase):    
	x = comentarios[comentarios['content'].str.contains(frase)] #selecionando apenas os comentarios com a frase de busca
	
	
	for mes in range(5,13): # de maio a dezembro de 2020
		t = comentarios[comentarios['date'].dt.month == mes]
		g = t[t['date'].dt.year == 2020]
		t1 = x[x['date'].dt.month == mes]
		g1 = t1[t1['date'].dt.year == 2020]
		print("Mes ", mes, " de 2020 ", len(g), len(g1), len(g1[g1['score'] <= 3]))
	
	for mes in range(1,6): #de janeiro a maio de 2021
		t = comentarios[comentarios['date'].dt.month == mes]
		g = t[t['date'].dt.year == 2021]
		t1 = x[x['date'].dt.month == mes]
		g1 = t1[t1['date'].dt.year == 2021]
		print("Mes ", mes, " de 2021 ", len(g), len(g1), len(g1[g1['score'] <= 3]) )    
	
def extractComments(Count:int,score:int = None):
	
	print("Extraindo comentarios com nota ", score)
	
	#creat empty lists to contain the fields acquired using google play scraper
	dates = []
	users_names = []
	contents = []
	scores = []
	version = []
	thumbs = []

	#acquire data 
	rvs, _ = gps.reviews(
		app_id,
		lang='pt',
		country='br',
		count= Count,
		filter_score_with= score
	)

	#fill lists with data acquired
	dates += [element["at"] for element in rvs] 
	contents += [element["content"] for element in rvs] 
	scores += [element["score"] for element in rvs] 
	version += [element["reviewCreatedVersion"] for element in rvs]
	thumbs += [element["thumbsUpCount"] for element in rvs]
	
	#use the filled list to create a single struct with all the acquired data, in the specified format
	reviews_df = pandas.DataFrame(data={ "date": dates,"content":contents, "score":scores, "version":version, "thumbs":thumbs } )
	
	for i in range(0, len(reviews_df)):
		if reviews_df['version'][i] == None:
			reviews_df = reviews_df.drop([i])
	return reviews_df

#extract and save 'Count' comments with each score 
#and if 'buildGeneral' is true, saves a file with all scores
def defaultExtraction(Count:int,buildGeneral=False):
	nameFile = "Data_Score"
	frames = []
	i = 1
	while i < 6:
		file = extractComments(Count,i)
		if buildGeneral:
			frames.append(file)
		file.to_csv(nameFile + str(i) + ".csv")
		i += 1
	if buildGeneral:	
		generalfile = pandas.concat(frames)
		generalfile.to_csv("General_Data.csv")

#defaultExtraction(2000,True)

for i in range(720):
	start_time = time.time()
	defaultExtraction(10000,True)
	UpdateOrCreateFile.update_Data()
	print("--- %s seconds ---" % (time.time() - start_time))
	time.sleep(3600)