import json
import scipy.io
import numpy
from sumy._compat import to_unicode
from sumy.models.dom import Sentence, Paragraph, ObjectDocumentModel
from sumy.nlp.tokenizers import Tokenizer 
import lex_rank_modified

def calc_quality(filename):

    with open(filename) as in_file:
        my_data = json.load(in_file)
    
    with open("stopwords.txt") as s_file:
        my_stopword_list = s_file.read().split()

    summarizer = lex_rank_modified.LexRankSummarizer()
    summarizer.stop_words = my_stopword_list

    matrix_dict = {}
    n_docs = 0
    for doc in my_data:
        processed_sents = list(map(to_sentence, doc['responses']))
        my_paragraphs = [Paragraph(processed_sents)]
        my_doc = ObjectDocumentModel(my_paragraphs)

        ratings = summarizer(my_doc)

        feat_matrix = numpy.matrix(ratings).transpose()
        qual_matrix = numpy.exp(feat_matrix)
        matrix_dict['q' + str(n_docs)] = qual_matrix
        n_docs += 1
        #print n_docs

    scipy.io.savemat('qual.mat', matrix_dict)
    return

def to_sentence(text):
    text = to_unicode(text).strip()
    return Sentence(text, Tokenizer("english"))

if __name__ == '__main__':
    calc_quality("aspect_query_responses_10192017_with_vecs.json")