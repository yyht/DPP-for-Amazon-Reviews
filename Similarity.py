import json
import scipy.io
from sklearn.feature_extraction.text import TfidfVectorizer

def calc_similarity():

    with open("reviews_by_seed.json") as in_file:
        data = json.load(in_file)

    with open("stopwords.txt") as s_file:
        stopword_list = s_file.read().split()

    docs = []
    num_docs = 0
    for kk in data:
        docs += data[kk]
        num_docs += 1

    #stopword_list = ['and','to','the','of']

    vectorizer = TfidfVectorizer(stop_words=stopword_list)
    tfidf_matrix = vectorizer.fit_transform(docs)

    md = {}
    for k in xrange(num_docs):
        curr_matrix = tfidf_matrix[k*100:(k+1)*100]
        sim_matrix = curr_matrix * curr_matrix.transpose()
        md['s' + str(k+1)] = sim_matrix.todense()

    scipy.io.savemat('sim.mat', md)
    return


if __name__ == '__main__':
    calc_similarity()




