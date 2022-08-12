#climate concept clustering for semantic equivalence determination

#plan:
# for each climate concept, create a wordtovec vector of 4 dimensions (change_direction, type_of, base, aspect_changing)
# for multi token components, take the average to get a single number for that position in the vector/array

#then make UMAP plots (or tSNE?) of the climate concept vectors. consider making a separate plot for all the 'increase' concepts separate than all the 'decrease' concepts.
#For now, ignore trying to equate equivalence through opposite concepts with opposite change_direction (even if they are semantically equivalent)



import pandas as pd
import spacy
import word2vec
import numpy as np


#load data
deduplicated_standardized_causal_relations_concepts_simple = pd.read_csv("/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_3_per_cluster_outputs/deduplicated_standardized_causal_relations_climate_concepts_simple_v1.csv")

standardized_data = pd.read_csv("/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_3_per_cluster_outputs/node standardization data processed v1.csv")

standardized_data = standardized_data[  standardized_data["base (standardized v1)"].notnull()  ]

standardized_data = standardized_data[[ "climate_concept_id", "change_direction (standardized v1)", "type_of (standardized v1)", "base (standardized v1)", "aspect_changing (standardized v1)", "climate_concept_string_representation" ]].drop_duplicates()

#subset and remove duplicates, then reset the index.

standardized_data["climate_concept_string_representation2"] = np.char.add(np.asarray([str(number) for number in standardized_data["climate_concept_id"].values]) , "_") + np.asarray(standardized_data["climate_concept_string_representation"].values)



standardized_data.reset_index(inplace=True)


nlp = spacy.load('en_core_web_md')


#bases_array = bases.concept_base.to_numpy()

climate_concept_indexes = standardized_data["climate_concept_id"]
change_direction_array = standardized_data["change_direction (standardized v1)"]
type_of_array = standardized_data["type_of (standardized v1)"]
base_array = standardized_data["base (standardized v1)"]
aspect_changing_array = standardized_data["aspect_changing (standardized v1)"]


multi_dimensional_array = []
one_dimensional_array = []

#for i in climate_concept_indexes:
for x in range(len(climate_concept_indexes)):
	climate_concept_index = climate_concept_indexes[x]
	
	change_direction = change_direction_array[x]
	change_direction_vector = nlp(change_direction).vector

	type_of = type_of_array[x]
	type_of_vector = nlp(type_of).vector

	base = base_array[x]
	base_vector = nlp(base).vector

	aspect_changing = aspect_changing_array[x]
	aspect_changing_vector = nlp(aspect_changing).vector

	to_add = [change_direction_vector, type_of_vector, base_vector, aspect_changing_vector]
	multi_dimensional_array.append(to_add)

	# print(len(change_direction_vector))
	# print(len(type_of_vector))
	# print(len(base_vector))
	# print(len(aspect_changing_vector))

	#to_add_concat2 = change_direction_vector + type_of_vector + base_vector + aspect_changing_vector
	to_add_concat = np.concatenate((change_direction_vector, type_of_vector, base_vector, aspect_changing_vector),axis=0)
	one_dimensional_array.append(to_add_concat)



#vector_exists_check = []
#has.vector check
#for base in bases_array:
#	vector_exists_check.append(nlp(base).vector.sum()!=0)

multi_dimensional_array_np = np.asarray(multi_dimensional_array)

#try to concatenate the 4 dimensions into 1d array
one_dimensional_array_np = np.asarray(one_dimensional_array)


from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering

# plt.figure(figsize=(70, 30))
# plt.title("Dendrogram of Climate Concepts")
# #dend = shc.dendrogram(shc.linkage(bases_vectors, method='ward'))
# dend = shc.dendrogram(shc.linkage(one_dimensional_array_np, method='average', metric='cosine'), labels=standardized_data.climate_concept_string_representation2.values)
#plt.show()
#dend = shc.dendrogram(shc.linkage(one_dimensional_array_np, method='average', metric='cosine'))

#plt.savefig('climate_concept_similarity_clustering.pdf') 



#263 and 362 are equivalent. 'increase_[]_environment_damage' & 'increase_[]_global sustainability_damage'


#try again... but with weighting... and make 2 separate plots. one for change_direction of increase and one for change_direction of decrease
# then give base a weight of 70%, aspect changing a weight of 20% and type_of a weight of 10% for clustering
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.weighted.html

#UPGMA algorithm vs WPGMA
#The WPGMA method is similar to its unweighted variant, the UPGMA method.
#https://stats.stackexchange.com/questions/77850/assign-weights-to-variables-in-cluster-analysis

#One way to assign a weight to a variable is by changing its scale. 
#Expressing a variable in smaller units will lead to a larger range for that variable, which will then have a large effect on the resulting structure. On the other hand, by standardizing one attempts to give all variables an equal weight, in the hope of achieving objectivity.

# https://stackoverflow.com/questions/45025056/how-to-perform-cluster-with-weights-density-in-python-something-like-kmeans-wit

#to do weighted clustering like we want, we have to define a custom distance metric. 

from numpy import dot
from numpy.linalg import norm

#from sklearn.metrics.pairwise import cosine_similarity
#cosine_similarity([[1, 0, -1]], [[-1,-1, 0]])

from sklearn.metrics.pairwise import cosine_similarity

import scipy

def cosine_similarity_function(u,v):
	u = u.reshape(1,-1)
	v = v.reshape(1,-1)
	result = 1 - cosine_similarity(u,v)[0][0]

	#result = np.clip(dmatr,0,1,dmatr)
	# result = scipy.clip(result, 0, 1)
	result = np.clip(result, 0, 1)


	return(result)


def custom_distance_metric(a, b, change_direction_weight, type_of_weight, base_weight, aspect_changing_weight):
	a_change_direction = a[0:300]
	b_change_direction = b[0:300]
	change_direction_cos_sim = cosine_similarity_function(a_change_direction, b_change_direction)

	a_type_of = a[300:600]
	b_type_of = b[300:600]
	type_of_cos_sim = cosine_similarity_function(a_type_of, b_type_of)

	a_base = a[600:900]
	b_base = b[600:900]
	base_cos_sim = cosine_similarity_function(a_base, b_base)

	a_aspect_changing = a[900:1200]
	b_aspect_changing = b[900:1200]
	aspect_changing_cos_sim = cosine_similarity_function(a_aspect_changing, b_aspect_changing)

	weight_vector = np.asarray([change_direction_weight, type_of_weight, base_weight, aspect_changing_weight])
	cos_sim_vector = np.asarray([change_direction_cos_sim, type_of_cos_sim, base_cos_sim, aspect_changing_cos_sim])

	final_distance = dot(weight_vector, cos_sim_vector)


	#scipy.spatial.distance.cosine #SLOW!

	return(final_distance)

#custom_pairwise_distance_metric = scipy.spatial.distance.pdist(X, lambda u, v: custom_distance_metric(u, v, 0.00, 0.10, 0.75, 0.25) )
#lambda x, y:

plt.figure(figsize=(70, 30))
plt.title("Dendrogram of Climate Concepts, weighted clustering")
#dend = shc.dendrogram(shc.linkage(bases_vectors, method='ward'))
# dend = shc.dendrogram(shc.linkage(one_dimensional_array_np, method='average', metric=lambda u, v: custom_distance_metric(u, v, 0.00, 0.00, 1.00, 0.00)), labels=standardized_data.climate_concept_string_representation2.values)
# dend = shc.dendrogram(shc.linkage(one_dimensional_array_np, method='average', metric=lambda u, v: custom_distance_metric(u, v, 0.00, 0.1, 0.7, 0.2)), labels=standardized_data.climate_concept_string_representation2.values)
# dend = shc.dendrogram(shc.linkage(one_dimensional_array_np, method='average', metric=lambda u, v: custom_distance_metric(u, v, 0.05, 0.0, 0.9, 0.05)), labels=standardized_data.climate_concept_string_representation2.values)
dend = shc.dendrogram(shc.linkage(one_dimensional_array_np, method='average', metric=lambda u, v: custom_distance_metric(u, v, 0.7, 0.05, 0.2, 0.05)), labels=standardized_data.climate_concept_string_representation2.values)


#plt.show()
#dend = shc.dendrogram(shc.linkage(one_dimensional_array_np, method='average', metric='cosine'))

# plt.savefig('climate_concept_similarity_clustering_with_weights_cd_0.0_t_0.0_b_1_a_0.00.pdf') 
# plt.savefig('climate_concept_similarity_clustering_with_weights_cd_0.0_t_0.1_b_0.7_a_0.2_fixed.pdf') 
# plt.savefig('climate_concept_similarity_clustering_with_weights_cd_0.05_t_0.0_b_0.9_a_0.05_fixed.pdf') 
plt.savefig('climate_concept_similarity_clustering_with_weights_cd_0.7_t_0.05_b_0.2_a_0.05_fixed.pdf') 






#the goal is to create equivalence classes (make sets of the 'climate concept ids')



# https://umap.scikit-tda.org/transform.html
# https://plotly.com/python/t-sne-and-umap-projections/
# https://towardsdatascience.com/umap-dimensionality-reduction-an-incredibly-robust-machine-learning-algorithm-b5acb01de568



