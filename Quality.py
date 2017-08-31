import json
import scipy.io
import numpy
from sumy._compat import to_unicode
from sumy.models.dom import Sentence, Paragraph, ObjectDocumentModel
from sumy.nlp.tokenizers import Tokenizer 
import lex_rank_modified

def calc_quality():

    with open("reviews_by_seed.json") as in_file:
        data = json.load(in_file)
    
    #TODO: Make use of stopword list
    with open("stopwords.txt") as s_file:
        stopword_list = s_file.read().split()

    k = 0
    p = []
    md = {}
    summarizer = lex_rank_modified.LexRankSummarizer()
    #summarizer.stop_words(stopword_list)

    for kk in data:
        prelim_doc = list(map(preprocess,data[kk]))
        s = list(map(to_sentence, prelim_doc))
        p.append(Paragraph(s))
        d = ObjectDocumentModel(p)
        ratings = summarizer(d)
        feat_matrix = numpy.matrix(ratings).transpose()
        qual_matrix = numpy.exp(feat_matrix)
        md['q' + str(k+1)] = qual_matrix
        k+=1
        p = []

    scipy.io.savemat('qual.mat', md)
    return

def preprocess(text):
    return to_unicode(text).strip()

def to_sentence(text):
    return Sentence(text, Tokenizer("english"))

if __name__ == '__main__':
    calc_quality()