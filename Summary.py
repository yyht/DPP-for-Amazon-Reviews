import json
import scipy.io

def gen_summary():

	with open("reviews_by_seed.json") as in_file:
		my_data = json.load(in_file)

	with open("sel.mat") as sel_file:
		select = scipy.io.loadmat('sel.mat')['Selections']

	doc_num = 0
	summ_dict = {}
	for keywords, sentences in my_data.iteritems():
		summ_dict['doc' + str(doc_num)] = [sentences[(i-1)] for i in select[doc_num]]
		doc_num += 1

	with open("summary.json", "w") as out_file:
		json.dump(summ_dict, out_file)

	return

if __name__ == '__main__':
	gen_summary()
