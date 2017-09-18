import json
import scipy.io
from sklearn.feature_extraction.text import TfidfVectorizer

def calc_similarity(filename):

    with open(filename) as in_file:
        my_data = json.load(in_file)

    with open("stopwords.txt") as s_file:
        my_stopword_list = s_file.read().split()

    my_docs = []
    n_docs = len(my_data)
    n_sents = []
    
    for doc in my_data:
        my_docs += doc['responses']
        n_sents.append(len(doc['responses']))

    vectorizer = TfidfVectorizer(stop_words = my_stopword_list)
    tfidf_matrix = vectorizer.fit_transform(my_docs)

    progress = 0
    matrix_dict = {}
    for k in xrange(n_docs):
        curr_matrix = tfidf_matrix[progress:progress + n_sents[k]]
        sim_matrix = curr_matrix * curr_matrix.transpose()
        matrix_dict['s' + str(k)] = sim_matrix.todense()
        progress += n_sents[k]

    scipy.io.savemat('sim.mat', matrix_dict)

    return

if __name__ == '__main__':
    calc_similarity("aspect_query_responses.json")