# script to read in the pickled file of all the pocket articles' text extracted using DiffBot.
# Then output as a JSON that is compatible for inputting into Protigy for text annotation.
# RRR: Argparse this

import pandas as pd
import pickle
#import jsonlines
import json

file_path = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/diffbot_and_pocket_tag_data/all_pocket_diffbot_extract.p"
compressed = open(file_path, "rb")
data = pickle.load(compressed)

tags_file_path = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/diffbot_and_pocket_tag_data/all_pocket_tag_annotations.csv"

# data[0]['objects'][0].keys()
# 'date', 'sentiment', 'images', 'author', 'estimatedDate', 'publisherRegion', 'icon', 'diffbotUri', 'siteName',
# 'type', 'title', 'tags', 'publisherCountry', 'humanLanguage', 'pageUrl', 'html', 'text'


output_file_path = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/all_pocket_for_prodigy2.jsonl"
#multi_output_folder = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/json_files/"

#read all pocket tag annotations csv file into pandas dataframe
tag_annotations = pd.read_csv(tags_file_path, sep = "\t")


# def all_different_1d(lst):
# 	return len(lst) == len(set(lst))


annotations_df = tag_annotations[["pageURL","tags"]]
annotations_df.tags = annotations_df["tags"].apply(lambda x: x.strip('][').replace("'","").split(', '))

#df.groupby(df.columns.tolist(),as_index=False).size()
#resolve duplicates by merging them.
annotations_df = annotations_df.groupby(['pageURL']).agg(sum).reset_index()
unique_tag_annotations = annotations_df.copy()
unique_tag_annotations.tags = annotations_df['tags'].apply(lambda x: list(set(x)))

# unique_tag_annotations['duplicate_tags'] = unique_tag_annotations["tags"].apply(all_different_1d)

#breakpoint()

text_list = []

for article in data:
	#breakpoint()

	try:
		article_json = article['objects']
		text_list.append(article_json)

		# if(article_json["type"]):
		# 	doc_type = article_json["type"]
		# 	if(doc_type == "article"):


		# text = article_json["text"]
		# unique_id = article_json["diffbotUri"]
		# url = article_json["pageUrl"]
		# title = article_json["title"]
		# tags = article_json["tags"]

		# date = article_json["date"]
		# author = article_json["author"]
		# siteName = article_json["siteName"]

		# items = {}
		# items["text", "title", "tags", "date", "author", "siteName", "unique_id", "url", "doc_type"] = [text, title, tags, date, author, siteName, unique_id, url, doc_type]

		# print("working")

		# #text_list.append(article_json)
		# text_list.append(items)

	except:
		print()#article.keys())


with open(output_file_path, 'w') as f:
    for item in text_list:
        f.write(json.dumps(item[0]) + "\n")





# output_file_path2 = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/all_pocket_for_prodigy3.jsonl"
# #multi_output_folder = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/json_files/"

# text_list = []

# for article in data:
# 	#breakpoint()

# 	try:
# 		article_json = article['objects']
# 		# text_list.append(article_json)

# 		if(article_json[0]["type"]):
# 			doc_type = article_json[0]["type"]
# 			if(doc_type == "article"):

# 				text = article_json[0]["text"]
# 				unique_id = article_json[0]["diffbotUri"]
# 				url = article_json[0]["pageUrl"]
# 				title = article_json[0]["title"]
# 				tags = article_json[0]["tags"]

# 				date = article_json[0]["date"]
# 				author = article_json[0]["author"]
# 				siteName = article_json[0]["siteName"]

# 				#items = {}
# 				items = {"text" : text, "title" : title, "tags": tags, "date": date, "author": author, "siteName": siteName, "unique_id": unique_id, "url": url, "doc_type": doc_type}
# 				#items = {"text" : text, "title" : title, "siteName": siteName, "url": url}

# 				print("working")
# 				text_list.append(items)

# 	except:
# 		print(article.keys())


# with open(output_file_path2, 'w') as f:
#     for item in text_list:
#         f.write(json.dumps(item) + "\n")





output_file_path3 = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/all_pocket_for_prodigy4.jsonl"
#multi_output_folder = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/json_files/"

text_list = []

for article in data:
	#breakpoint()

	try:
		article_json = article['objects']
		# text_list.append(article_json)

		if(article_json[0]["type"]):
			doc_type = article_json[0]["type"]
			if(doc_type == "article"):

				text = article_json[0]["text"]
				#unique_id = article_json[0]["diffbotUri"]
				url = article_json[0]["pageUrl"]
				title = article_json[0]["title"]
				#tags = article_json[0]["tags"]

				#date = article_json[0]["date"]
				#author = article_json[0]["author"]
				siteName = article_json[0]["siteName"]

				#items = {}
				#items = {"text" : text, "title" : title, "tags": tags, "date": date, "author": author, "siteName": siteName, "unique_id": unique_id, "url": url, "doc_type": doc_type}
				items = {"text" : text, "title" : title, "siteName": siteName, "url": url}

				#print("working")
				text_list.append(items)

	except:
		print(article.keys())


with open(output_file_path3, 'w') as f:
    for item in text_list:
        f.write(json.dumps(item) + "\n")








#split sentences
output_file_path4 = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/all_pocket_for_prodigy5.jsonl"
#multi_output_folder = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/json_files/"

text_list = []

for article in data:
	#breakpoint()

	try:
		article_json = article['objects']
		# text_list.append(article_json)

		if(article_json[0]["type"]):
			doc_type = article_json[0]["type"]
			if(doc_type == "article"):

				text = article_json[0]["text"]
				#unique_id = article_json[0]["diffbotUri"]
				url = article_json[0]["pageUrl"]
				title = article_json[0]["title"]
				#diffbot_tags = article_json[0]["tags"]

				#date = article_json[0]["date"]
				#author = article_json[0]["author"]
				siteName = article_json[0]["siteName"]

				if(url in unique_tag_annotations['pageURL'].tolist()):
					pocket_tags = unique_tag_annotations.loc[ unique_tag_annotations['pageURL'] == url , "tags"].tolist()[0]

				#items = {}
				#items = {"text" : text, "title" : title, "diffbot_tags": tags, "date": date, "author": author, "siteName": siteName, "unique_id": unique_id, "url": url, "doc_type": doc_type}

				if(pocket_tags):
					items = {"text" : text, "title" : title, "siteName": siteName, "url": url, "pocket_tags": ", ".join(pocket_tags)}
				else:
					items = {"text" : text, "title" : title, "siteName": siteName, "url": url}

				#print("working")
				text_list.append(items)

	except:
		print(article.keys())


with open(output_file_path4, 'w') as f:
    for item in text_list:
        f.write(json.dumps(item) + "\n")




#split sentences
output_file_path5 = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/all_pocket_for_prodigy_effect_tag_texts_only.jsonl"
#multi_output_folder = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/json_files/"

text_list = []

for article in data:
	#breakpoint()

	try:
		article_json = article['objects']
		# text_list.append(article_json)

		if(article_json[0]["type"]):
			doc_type = article_json[0]["type"]
			if(doc_type == "article"):

				text = article_json[0]["text"]
				#unique_id = article_json[0]["diffbotUri"]
				url = article_json[0]["pageUrl"]
				title = article_json[0]["title"]
				#diffbot_tags = article_json[0]["tags"]

				#date = article_json[0]["date"]
				#author = article_json[0]["author"]
				siteName = article_json[0]["siteName"]

				if(url in unique_tag_annotations['pageURL'].tolist()):
					pocket_tags = unique_tag_annotations.loc[unique_tag_annotations['pageURL'] == url , "tags"].tolist()[0]

				#items = {}
				#items = {"text" : text, "title" : title, "diffbot_tags": tags, "date": date, "author": author, "siteName": siteName, "unique_id": unique_id, "url": url, "doc_type": doc_type}

				if(pocket_tags):
					items = {"text" : text, "title" : title, "siteName": siteName, "url": url, "pocket_tags": ", ".join(pocket_tags)}
				else:
					items = {"text" : text, "title" : title, "siteName": siteName, "url": url}

				#print("working")
				if("effects" in pocket_tags):
					text_list.append(items)

	except:
		print(article.keys())


with open(output_file_path5, 'w') as f:
    for item in text_list:
        f.write(json.dumps(item) + "\n")
