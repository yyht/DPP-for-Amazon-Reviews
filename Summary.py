import json
import scipy.io

def gen_summary(filename):

	with open(filename) as in_file:
		my_data = json.load(in_file)

	with open("sel.mat") as sel_file:
		select = scipy.io.loadmat('sel.mat')['selections']

	#keys_sort = sorted(my_data.keys())

	doc_num = 0
	#summary = []
	for doc in my_data:
		#curr_dict = {'aspect': doc['aspect'], 'keyword': doc['keyword']}

		doc['responses'] = [doc['responses'][(i-1)] for i in select[doc_num] if i != -1]
		doc_num += 1
		print doc_num
		#print doc['keyword']
		#summary.append(curr_dict)

	with open("summary.json", "w") as out_file:
		json.dump(my_data, out_file)

	return

if __name__ == '__main__':
	gen_summary("aspect_query_responses.json")
