
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans as kmeans
from sklearn.decomposition import NMF
#################################################################
#Combining the negative and positive reviews in file directory into seperate lists

final_doc_pos=[]
final_doc_neg=[]
directory="/home/kamran/Desktop"
for filename in os.listdir(directory):	
	if filename.startswith("pos"):
		fpos=open(filename).readlines()		
		fpos1=[x.strip() for x in fpos]		
		for i in fpos1:		
			final_doc_pos.append(i)

	elif filename.startswith("neg"):
		fneg=open(filename).readlines()
		fneg1=[y.strip() for y in fneg]
		for r in fneg1:
			final_doc_neg.append(r)

final_doc=final_doc_pos+final_doc_neg
######################################################################

# TF-IDF Transformation
vect=TfidfVectorizer(stop_words="english", lowercase=True, max_features=100, norm="l2")
doc_tfidf=vect.fit_transform(final_doc) # TF_IDF transformation of the document

#K- means Clustering

num_clus=2 #num of clusters to be formed
clus_mod=kmeans(n_clusters=num_clus,max_iter=50, init='k-means++')
clus_mod.fit(doc_tfidf) # fitting the k- means clustering on the final doc

print("Top terms per cluster:")
centroid_ord = clus_mod.cluster_centers_.argsort()[:, ::-1]
terms = vect.get_feature_names()
for i in range(num_clus):
    print("Cluster %d:" % i),
    for ind in centroid_ord[i, :10]:
        print(' %s' % terms[ind]),
    print
########################################################################

# Topic finding using non-negative matrix factorization
	
nmf = NMF(n_components=5, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(doc_tfidf)


def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print ("Topic %d:" % (topic_idx))
        print (" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
						
no_top_words = 10
display_topics(nmf, terms, no_top_words)
