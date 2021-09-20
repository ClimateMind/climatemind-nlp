#script to analyze inter-annotator agreement
import pandas as pd
from functools import reduce 


data_file = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/checkin_three_all_labels_interannotator_agreement_data_setup_09-18-2021_132540 - checkin_three_all_labels_interannotator_agreement_data_setup_09-18-2021_132540.csv"

#read in the data
data = pd.read_csv(data_file)

column_names = list(data.columns)

#filter to just be feature=='entity'
data_entity = data[data['feature']=="entity"]

#filter to remove 'answers' from the annotations
data_entity = data_entity[data_entity['annotator']!="answers"]

#for each token (word) of every sentence, what are the range of 'types' for the feature 'entity' and for a given token which type has the max agreement % and what is that %?
#and count how many unique 'type' fields represented in each and save the output
grouped = data_entity.groupby(by=["sentence", "document id", "sentence id", "word", "token number"], as_index=False)

#https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#groupby-aggregate-named

# columns with counts for each entity type possible
# column for total number of annotators for that sentence
# column for number of unique different types 
# column for entity type with the most number of counts
# % agreement for the most popular annotation
result = grouped.agg(
	none_count=pd.NamedAgg(column="type", aggfunc=lambda x: x[x== 'None'].count()),
	base_count=pd.NamedAgg(column="type", aggfunc=lambda x: x[x== 'base'].count()),
	type_of_count=pd.NamedAgg(column="type", aggfunc=lambda x: x[x== 'type_of'].count()),
	aspect_changing_count=pd.NamedAgg(column="type", aggfunc=lambda x: x[x== 'aspect_changing'].count()),
	change_direction_count=pd.NamedAgg(column="type", aggfunc=lambda x: x[x== 'change_direction'].count()),
	to_whom_count=pd.NamedAgg(column="type", aggfunc=lambda x: x[x== 'to_whom'].count()),
	where_count=pd.NamedAgg(column="type", aggfunc=lambda x: x[x== 'where'].count()),
	when_count=pd.NamedAgg(column="type", aggfunc=lambda x: x[x== 'when'].count()),
	effect_size_count=pd.NamedAgg(column="type", aggfunc=lambda x: x[x== 'effect_size'].count()),
	confidence_count=pd.NamedAgg(column="type", aggfunc=lambda x: x[x== 'confidence'].count()),
	predicate_count=pd.NamedAgg(column="type", aggfunc=lambda x: x[x== 'predicate'].count()),
	annotators_total=pd.NamedAgg(column="type", aggfunc="count"),
	unique_annotations=pd.NamedAgg(column="type", aggfunc="nunique"),
	max_agreement=pd.NamedAgg(column="type", aggfunc=lambda x:x.value_counts()[0]/x.count()*100),
	most_popular=pd.NamedAgg(column="type", aggfunc=lambda x: pd.Series.mode(x)),
	popularity_tie=pd.NamedAgg(column="type", aggfunc=lambda x: pd.Series.mode(x).count()>1)
	)


result["max_agreement"] = result.max_agreement.round(2)


# columns for annotator names that are in the agreement and not in the agreement
joined_data = data_entity.merge(result, on=["document id", "sentence id", "word", "token number"])

agreement_annotators = joined_data.loc[joined_data.apply(lambda x: x["type"] in x["most_popular"], axis=1),["annotator", "document id", "sentence id", "word", "token number"]]

disagreement_annotators = joined_data.loc[joined_data.apply(lambda x: x["type"] not in x["most_popular"], axis=1),["annotator", "document id", "sentence id", "word", "token number"]]

grouped_agreement_annotators = agreement_annotators.groupby(by=["document id", "sentence id", "word", "token number"])["annotator"].apply(", ".join).reset_index()

grouped_disagreement_annotators = disagreement_annotators.groupby(by=["document id", "sentence id", "word", "token number"])["annotator"].apply(", ".join).reset_index()

grouped_agreement_annotators["agreement_annotators"] = grouped_agreement_annotators["annotator"]
grouped_disagreement_annotators["disagreement_annotators"] = grouped_disagreement_annotators["annotator"]

result_final = result.merge(grouped_agreement_annotators[["document id", "sentence id", "word", "token number","agreement_annotators"]], on=["document id", "sentence id", "word", "token number"])
result_final = result_final.merge(grouped_disagreement_annotators[["document id", "sentence id", "word", "token number", "disagreement_annotators"]], on=["document id", "sentence id", "word", "token number"])



#save the result as output file
output_path = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/checkin_three_all_labels_interannotator_agreement_data_setup_09-18-2021_132540 - checkin_three_all_labels_interannotator_agreement_data_setup_09-18-2021_132540 entity interannotator agreement.csv"
result_final.to_csv(output_path)


#https://pbpython.com/groupby-agg.html
#https://medium.com/escaletechblog/writing-custom-aggregation-functions-with-pandas-96f5268a8596
#https://towardsdatascience.com/creating-custom-aggregations-to-use-with-pandas-groupby-e3f5ef8cb43e
#https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.aggregate.html
#https://jakevdp.github.io/PythonDataScienceHandbook/03.08-aggregation-and-grouping.html
#https://stackoverflow.com/questions/45752601/how-to-do-a-conditional-count-after-groupby-on-a-pandas-dataframe
#grouped['type'].aggregate({'none_count': none_count}, {'base_count': base_count})
#grouped.aggregate(none_count)
#https://deanla.com/pandas_named_agg.html





