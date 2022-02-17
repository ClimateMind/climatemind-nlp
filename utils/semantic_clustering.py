#semantic clustering either with word2vec, sense2vec, or methods leveraging wordnet

import spacy
import word2vec

#https://ashutoshtripathi.com/2020/09/04/word2vec-and-semantic-similarity-using-spacy-nlp-spacy-series-part-7/

#https://spacy.io/models/en#en_vectors_web_lg
#https://spacy.io/models/en#en_core_web_lg
#https://spacy.io/models/en#en_core_web_md

#python -m spacy download en_core_web_md
#python -m spacy download en_core_web_lg
#python -m spacy download en_vectors_web_lg 
import pandas as pd
import numpy as np

bases = pd.read_csv("reduced_concept_bases.csv")

bases_array = bases.concept_base.to_numpy()

nlp = spacy.load('en_core_web_md')


vector_exists_check = []
#has.vector check
for base in bases_array:
	vector_exists_check.append(nlp(base).vector.sum()!=0)

vector_check = np.asarray(vector_exists_check)

base_indexes_to_remove = np.where(vector_check == False)
unclusterable_bases = bases_array[base_indexes_to_remove]

bases_clusterable = np.delete(bases_array, base_indexes_to_remove)

#identifying similar vectors

#get the vectors for each word

#nlp.vocab[bases_array[0]].vector
nlp(bases_array[0]).vector

vectors = []

for base in bases_array:
	vectors.append(nlp(base).vector)

bases_vectors = np.asarray(vectors)

vectors_clusterable = np.delete(bases_vectors, base_indexes_to_remove, axis=0)


#visualize using agglomerative heirarchical clustering
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
import scipy.cluster.hierarchy as shc
from sklearn.datasets import load_iris
from sklearn.cluster import AgglomerativeClustering

#cluster = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward')
#cluster.fit_predict(X)
#print(cluster.labels_)

#https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html

#https://stackabuse.com/hierarchical-clustering-with-python-and-scikit-learn/

plt.figure(figsize=(30, 10))
plt.title("Dendrogram of Bases from Climate Concepts")
#dend = shc.dendrogram(shc.linkage(bases_vectors, method='ward'))
dend = shc.dendrogram(shc.linkage(vectors_clusterable, method='average', metric='cosine'), labels=bases_clusterable)
#plt.show()

plt.savefig('base_similarity_clustering.pdf') 
#plt.savefig('base_similarity_clustering2.pdf', dpi=300)  







