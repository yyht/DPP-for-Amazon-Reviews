import json
import scipy.io
import numpy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer 
import Importance

def calc_quality():

    with open("reviews_by_seed.json") as in_file:
        data = json.load(in_file)
    
    sep = " "
    docs = []
    num_docs = 0
    for kk in data:
        for sentence in range(len(data[kk])):
            data[kk][sentence] = data[kk][sentence].replace('.',' ')+'.'

        docs.append(sep.join(data[kk]))
        num_docs += 1
    
    summarizer = Importance.LexRankSummarizer()
    theta = numpy.ones(1)
    md = {}
    for k in xrange(num_docs):
        parser = PlaintextParser.from_string(docs[k], Tokenizer("english"))
        ratings = summarizer(parser.document)
        feat_matrix = numpy.matrix(ratings).transpose()
        qual_matrix = numpy.exp(feat_matrix*theta)
        md['q' + str(k+1)] = qual_matrix

    scipy.io.savemat('qual.mat', md)
    return


if __name__ == '__main__':
    calc_quality()