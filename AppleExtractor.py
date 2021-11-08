import pandas
from app_store_scraper import AppStore

app = AppStore(country="br", app_name="gov.br")
app.review(how_many=2000)

dates = []
isEdited = []
rating = []
review = []
title = []
username = []

	#fill lists with data acquired

for line in app.reviews:
	dates.append(line['date'])
	rating.append(line['rating']) 
	title.append(line['title'])  
	review.append(line['review']) 


reviews_df = pandas.DataFrame(data={ "date": dates,"content":review,"title":title, "score":rating} )
reviews_df.to_csv("General_Apple.csv")