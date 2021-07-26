#convert data to longform. only take 'change_direction', 'type_of', 'base', 'aspect_changing', 'text'
#for each entity that has multiples, expand the concept into multiple rows with each possible permutation (uses Cartesian product)

import pandas as pd
from itertools import product
import spacy
import srsly


#read in csv file
#make sure read it in correctly! As of now it's reading in the square brackets as strings and not as list items!

file_path = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/checkin_answers_concepts_export.csv"
data = pd.read_csv(file_path) 

all_rows = []

#for each row in the pandas dataframe... and build new dataframe
#for index, row in df.iterrows():
for row in data.itertuples():
	change_direction = getattr(row, "change_direction")
	type_of = getattr(row, "type_of")
	base = getattr(row, "base")
	aspect_changing = getattr(row, "aspect_changing")
	
	to_whom = getattr(row, "to_whom")[0]
	effect_size = getattr(row, "effect_size")[0]
	confidence = getattr(row, "confidence")[0]
	where = getattr(row, "where")[0]
	when = getattr(row, "when")[0]
	predicate = getattr(row, "predicate")[0]
	
	text = getattr(row, "text")[0]
	original_text = getattr(row, "original_text")[0]
	source = getattr(row, "source")[0]
	document_id = getattr(row, "document_id")[0]
	sentence_id = getattr(row, "sentence_id")[0]
	username = getattr(row, "username")[0]
	flag = getattr(row, "flag")[0]

	#new_rows_tuple = product(change_direction, type_of, base, aspect_changing)
	new_rows = (list(tup) for tup in product(change_direction, type_of, base, aspect_changing))

 	#for i in range(len(new_rows)):
 	#new_rows[i] = new_rows[i].extend([
	for i in new_rows:
 		new_row = i.extend([
 			to_whom, 
 			effect_size, 
 			confidence, 
 			where, 
 			when, 
 			predicate, 
 			text, 
 			original_text, 
 			source, 
 			document_id, 
 			sentence_id, 
 			username, 
 			flag
 			])
 		all_rows.append(new_row)

row_names = pd.Series([
'change_direction', 
'type_of', 
'base', 
'aspect_changing',

'to_whom',
'effect_size',
'confidence',
'where',
'when',
'predicate',

'text',
'original_text',
'source',
'document_id',
'sentence_id',
'username',
'flag'
])

core_concept_entities = ['change_direction', 'type_of', 'base', 'aspect_changing']
everything_not_core_concept_related = row_names[row_names.isin(core_concept_entities) == False]

#make lengthened dataframe that doesn't have lists for values
df = pd.DataFrame(all_rows, columns=[row_names])

#convert to longform data 
longform_data = pd.melt(df, 
	id_vars = everything_not_core_concept_related,
	value_vars = core_concept_entities ,
	var_name = "core_concept_entity",
	value_name = "phrase" )


#run diversity analysis
grouped = longform_data.groupby(by=["core_concept_entity", "phrase"], as_index=False)
#count how many unique 'text' fields represented in each and save the output
diversity_counts = grouped[['text']].value_counts()
diversity_counts2 = grouped[['text']].count()

#save results
diversity_counts.to_csv("diversity_counts.csv")
diversity_counts2.to_csv("diversity_counts2.csv")


# for ind in df.index:
#      print(df['Name'][ind], df['Stream'][ind])

# for i in range(len(df)) :
#   print(df.loc[i, "Name"], df.loc[i, "Age"]

# for index, row in df.iterrows():
#     print (row["Name"], row["Age"])


# for row in df.itertuples(index = True, name ='Pandas'):
#     print (getattr(row, "Name"), getattr(row, "Percentage"))




