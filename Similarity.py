import json
import scipy.io
import numpy as np
#from sklearn.feature_extraction.text import TfidfVectorizer

def calc_similarity(filename):

    with open(filename) as in_file:
        my_data = json.load(in_file)

    with open("stopwords.txt") as s_file:
        my_stopword_list = s_file.read().split()
    
    matrix_dict = {}
    k = 0

    for doc in my_data:
        vecs = np.array(doc['vecs'])
        vecs = np.dot(vecs, vecs.T)
        matrix_dict['s' + str(k)] = vecs #.todense()
        k += 1

    scipy.io.savemat('sim.mat', matrix_dict)

    return

if __name__ == '__main__':
    calc_similarity("aspect_query_responses_10192017_with_vecs.json")