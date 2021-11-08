import pandas
from app_store_scraper import AppStore

def get_Apple_Comments(score:int = None):

	if score:
		print("Getting score: ",score)
	else:
		print("Getting general data")
	app = AppStore(country="br", app_name="gov.br")
	app.review(how_many=2000)

	dates = []
	rating = []
	review = []
	title = []

		#fill lists with data acquired

	if score:
		for line in app.reviews:
			if int(line['rating']) == score:
				dates.append(line['date'])
				rating.append(line['rating']) 
				title.append(line['title'])  
				review.append(line['review'])

		reviews_df = pandas.DataFrame(data={ "date": dates,"content":review,"title":title, "score":rating} )
		name  = "Apple_Score" + str(score) + ".csv"
		reviews_df.to_csv(name)
	else:
		for line in app.reviews:
			dates.append(line['date'])
			rating.append(line['rating']) 
			title.append(line['title'])  
			review.append(line['review']) 

		reviews_df = pandas.DataFrame(data={ "date": dates,"content":review,"title":title, "score":rating} )
		reviews_df.to_csv("General_Apple.csv")

i = 1
while i < 6:
	get_Apple_Comments(i)
	i += 1
get_Apple_Comments()