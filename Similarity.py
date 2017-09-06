import json
import scipy.io
from sklearn.feature_extraction.text import TfidfVectorizer

def calc_similarity(n_sents):

    with open("reviews_by_seed.json") as in_file:
        my_data = json.load(in_file)

    with open("stopwords.txt") as s_file:
        my_stopword_list = s_file.read().split()

    my_docs = []
    n_docs = 0
    for keywords, sentences in my_data.iteritems():
        my_docs += sentences
        n_docs += 1

    vectorizer = TfidfVectorizer(stop_words = my_stopword_list)
    tfidf_matrix = vectorizer.fit_transform(my_docs)

    matrix_dict = {}
    for k in xrange(n_docs):
        curr_matrix = tfidf_matrix[k*n_sents:(k+1)*n_sents]
        sim_matrix = curr_matrix * curr_matrix.transpose()
        matrix_dict[my_data.keys()[k]] = sim_matrix.todense()

    scipy.io.savemat('sim.mat', matrix_dict)

    return


if __name__ == '__main__':
    calc_similarity(100)