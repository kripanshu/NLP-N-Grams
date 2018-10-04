import sys, re
from collections import Counter
from decimal import *

corpus_file = sys.argv[1]
sentence1 = sys.argv[2]
sentence2 = sys.argv[3]


class BigramModel(object):

    def __init__(self, corpus_file, sentence1, sentence2):
        self.corpus = self.get_corpus(corpus_file)
        self.sentence1_array = sentence1.split(" ");
        self.sentence2_array = sentence2.split(" ");
        self.bigram_sentence1 = []
        self.bigram_sentence2 = []
        self.sentence1_dict_without_smoothing = {}
        self.sentence2_dict_without_smoothing = {}
        self.sentence1_dict_with_smoothing = {}
        self.sentence2_dict_with_smoothing = {}
        self.words_count = 0 # words count in corpus
        self.prob_keep = []
        if "." in self.sentence1_array:
            del self.sentence1_array[-1]
        if "." in self.sentence2_array:
            del self.sentence2_array[-1]

        self.len1 = len(self.sentence1_array)
        self.len2 = len(self.sentence2_array)
        self.filler_matrix1_withoutSmoothing = [[0] * self.len1 for i in range(self.len1)]
        self.filler_matrix2_withoutSmoothing = [[0] * self.len2 for i in range(self.len2)]
        self.prob_matrix1_withoutSmoothing = [[0] * self.len1 for i in range(self.len1)]
        self.prob_matrix2_withoutSmoothing = [[0] * self.len2 for i in range(self.len2)]
        self.filler_matrix1_withSmoothing = [[0] * self.len1 for i in range(self.len1)]
        self.filler_matrix2_withSmoothing = [[0] * self.len2 for i in range(self.len2)]
        self.prob_matrix1_withSmoothing = [[0] * self.len1 for i in range(self.len1)]
        self.prob_matrix2_withSmoothing = [[0] * self.len2 for i in range(self.len2)]
        # print(" our sentence1 array", sentence1_array)
        # print(" our sentence2 array", sentence2_array)

    def runner_function(self):
        print("--"*50)
        print("Sentence 1 : ", sentence1)
        print("Sentence 2 : ", sentence2)
        print("###"*40)
        print(" ")

        self.bigram_creator(self.sentence1_array, self.sentence2_array)
        self.get_count_withoutSmoothing(self.sentence1_array, self.len1, "facebook1")
        self.get_count_withoutSmoothing(self.sentence2_array, self.len2, "facebook2")

        print(" ")
        print("###"*40)
        print("\t\t  Count Table without Smoothing Sentence 1 \t \t ")
        self.create_table(self.sentence1_array, self.filler_matrix1_withoutSmoothing)
        print(" ")
        print("###"*40)
        print(" \t\t  Count Table without Smoothing Sentence 2 \t \t ")
        self.create_table(self.sentence2_array, self.filler_matrix2_withoutSmoothing)
        print(" ")
        print("###"*40)
        print("\t\t  Probability Table without Smoothing sentence 1 \t \t  ")
        self.create_table(self.sentence1_array, self.prob_matrix1_withoutSmoothing)
        print(" ")
        print("###"*40)
        print("\t\t  Probability Table without Smoothing sentence 2 \t \t   ")
        self.create_table(self.sentence2_array, self.prob_matrix2_withoutSmoothing)

        self.get_count_withSmoothing(self.sentence1_array, self.len1, "facebook1")
        self.get_count_withSmoothing(self.sentence2_array, self.len2, "facebook2")
        print(" ")
        print("###"*40)
        print("\t\t  Count Table with Smoothing Sentence 1 \t \t ")
        self.create_table(self.sentence1_array, self.filler_matrix1_withSmoothing)
        print(" ")
        print("###"*40)
        print(" \t\t  Count Table with Smoothing Sentence 2 \t \t")
        self.create_table(self.sentence2_array, self.filler_matrix2_withSmoothing)
        print(" ")
        print("###"*40)
        print("\t\t  Probability Table with Smoothing sentence 1 \t \t   ")
        self.create_table(self.sentence1_array, self.prob_matrix1_withSmoothing)
        print(" ")
        print("###"*40)
        print("\t\t  Probability Table with Smoothing sentence 2 \t \t   ")
        self.create_table(self.sentence2_array, self.prob_matrix2_withSmoothing)
        print(" ")
        print("###"*40)
        print(" ")
        self.cal_prob(self.bigram_sentence1, self.sentence1_dict_without_smoothing, "without Smoothing", "sentence1")
        self.cal_prob(self.bigram_sentence2, self.sentence2_dict_without_smoothing, "without Smoothing","sentence2")
        self.cal_prob(self.bigram_sentence1, self.sentence1_dict_with_smoothing, "with Smoothing","sentence1")
        self.cal_prob(self.bigram_sentence2, self.sentence2_dict_with_smoothing, "with Smoothing","sentence2")
        print(" ")
        print("###"*40)
        print(" ")
        self.get_highest_prob(self.prob_keep)


    def get_highest_prob(self, prob_keep):
        high = 0
        sent = ""
        for item in prob_keep:
            if item['prob'] > high:
                high = item['prob']
                sent = item['name']

        print(sent + " has more Probability than the other")

    def get_corpus(self, courpus_file):
        file = open(corpus_file, 'r')
        stringForm = ""
        tokens = []
        for item in file:
            # print("%"*100)
            # print(item.strip())
            stringForm = stringForm + item.strip() + " "
        regex_string = re.sub('[^A-Za-z0-9\s]', ' ', stringForm)
        for i in regex_string.split():
		if len(i.strip().lower()) > 1:
			tokens.append(i.strip().lower())
        # print(regex_string)

        words_freq = Counter(tokens)
        # print(words_freq)
        self.words_count = len(words_freq)
        # print(words_freq)
        return regex_string

    def bigram_creator(self, sentence1_array, sentence2_array):
        # print(" our sentence1 array", sentence1_array)
        # print(" our sentence2 array", sentence2_array)

        for i in range(1,self.len1):
            pos_value = sentence1_array[i]+" "+sentence1_array[i-1]
            self.bigram_sentence1.append(pos_value)
        print("Bigrams creation for sentence 1 :",self.bigram_sentence1)
        for j in range(1,self.len2):
            pos_value = sentence2_array[j]+" "+sentence2_array[j-1]
            self.bigram_sentence2.append(pos_value)
        print("Bigrams creation for sentence 2 : ",self.bigram_sentence2)

    def create_table(self, sentence_array, matrix):
        print (self.printTable(sentence_array, matrix, '{:^{}}', '{:<{}}', '{:>{}}', '\n', ' | '))

    def get_count_withoutSmoothing(self, sentence_array, len1, sentence_name):
        input_string = self.corpus

        for i in range(0,len1):
            for j in range(0,len1):
                    sub_str = sentence_array[i]+" "+ sentence_array[j]
                    # print(sub_str)
                    # print(" ")
                    c = input_string.count(" "+sub_str+" ")
                    n = input_string.count(sentence_array[i])
                    # print(c, " and ", n)
                    prob = Decimal(c) /Decimal(n)

                    if sentence_name is "facebook1":

                        self.filler_matrix1_withoutSmoothing[i][j]=c
                        self.prob_matrix1_withoutSmoothing[i][j]= round(prob,3)
                        self.sentence1_dict_without_smoothing[sub_str]= {"count":c,"prob":round(prob,3)}
                    else:

                        self.filler_matrix2_withoutSmoothing[i][j]=c
                        self.prob_matrix2_withoutSmoothing[i][j]= round(prob,3)
                        self.sentence2_dict_without_smoothing[sub_str]={"count":c,"prob":round(prob,3)}
        # print(self.sentence1_dict_without_smoothing)
        # print(self.sentence2_dict_without_smoothing)

    def get_count_withSmoothing(self, sentence_array, len1, sentence_name):
        input_string = self.corpus

        for i in range(0,len1):
            for j in range(0,len1):
                    sub_str = sentence_array[i]+" "+ sentence_array[j]
                    # print(sub_str)
                    # print(" ")
                    c = input_string.count(" "+sub_str+" ")
                    n = input_string.count(sentence_array[i])
                    # print(c, " and ", n)
                    prob = Decimal(c+1) / Decimal(n+self.words_count)

                    if sentence_name is "facebook1":

                        self.filler_matrix1_withSmoothing[i][j]=c+1
                        self.prob_matrix1_withSmoothing[i][j]= round(prob,4)
                        self.sentence1_dict_with_smoothing[sub_str]= {"count":c,"prob":round(prob,4)}
                    else:

                        self.filler_matrix2_withSmoothing[i][j]=c+1
                        self.prob_matrix2_withSmoothing[i][j]= round(prob,4)
                        self.sentence2_dict_with_smoothing[sub_str]={"count":c,"prob":round(prob,4)}
        # print(self.sentence1_dict_without_smoothing)
        # print(self.sentence2_dict_without_smoothing)

    def cal_prob(self, bigram_sentence, input_dict, type, name_val):
        # print(bigram_sentence)
        # print(input_dict)
        sentence_name = name_val
        prob_value = 1
        for item in bigram_sentence:
            if item in input_dict:
                # print(item, " : ", input_dict[item]['prob'])
                prob_value *= input_dict[item]['prob']
        if type == "with Smoothing":
            out = "Probability of " + sentence_name + " with Smoothing is :"
            print(out)
            print(prob_value)
            self.prob_keep.append({"prob": prob_value, "name": sentence_name})
        elif type == "without Smoothing":
            out="Probability of "+ sentence_name+ " without Smoothing is :"
            print(out)
            print(prob_value)

    #Function to print the matrix [table]
    def printTable(self,rowColName, listVal,
                      topRow, leftBorder, dataLength, rowSep, colSep):

        table = [[''] + rowColName] + [[name] + row for name, row in zip(rowColName, listVal)]
        tableStructure = [['{:^{}}'] + len(rowColName) * [topRow]] \
                     + len(listVal) * [[leftBorder] + len(rowColName) * [dataLength]]
        columnLength = [max(len(format.format(cell, 0))
                          for format, cell in zip(col_format, col))
                      for col_format, col in zip(zip(*tableStructure), zip(*table))]
        return rowSep.join(
                   colSep.join(
                       format.format(cell, width)
                       for format, cell, width in zip(row_format, row, columnLength))
                   for row_format, row in zip(tableStructure, table))

if __name__ == '__main__':
    # creates an instance of the class
    bigram_inst = BigramModel(corpus_file, sentence1, sentence2)
    bigram_inst.runner_function()
