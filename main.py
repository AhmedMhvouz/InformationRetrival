import math
import os
from itertools import chain
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, lancaster
from nltk.tokenize import TweetTokenizer
from natsort import natsorted
# nltk.download('punkt')
# nltk.download('stopwords')
'''
first part 
1. read 10 txt files
2. Text Processing => intial stage  
    1. tokenization  
    2. stop words 
'''
stop_words = set(stopwords.words('english'))
stemmer = lancaster.LancasterStemmer()
str1 = ""  # text of all files
no_stpwords_string = ""  # result text
fileno = 0
pos_index = {}
file_map = {}
# path of folder which contain txt files
path = "E:/2- FCAI-HU/LV-4/Semester-1/IR/Project/IR_Pro/txt files"
folder_names = ["C:/Users/sayed/Downloads/Ir project/Ir project/ir"]
# change current dir to "path"
os.chdir(path)
# Read txt Files
def read_text_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        data = f.readlines()
    f.close()
    return data  # return all of txt content to tokenize them
def normalizing(string):
    # loop over files
    for file in os.listdir():  # list files in the current dir => path
        if file.endswith(".txt"):  # get .txt file only
            file_path = f"{path}\{file}"
            # read each file + tokenize it => save in 2D list
            tokens = [nltk.word_tokenize(i) for i in read_text_file(file_path)]
            # flat result to 1D list
            flatten_list = list(chain.from_iterable(tokens))
        # remove stop words from list
        for i in flatten_list:
            if not i.lower() in stop_words:
                string += i + ' ' # no_stpwords_string
    return string
# tokenized and free stop word text
# print(normalizing(no_stpwords_string))
'''
positional index
1. Build positional index
2. users phrase query => returns matched documents.
'''
'''
{
    "hello" : # word 
    [5, # number of appearing in files 
    [ 
        {3 : # number of first file 
            [3, # number of appearing in this file 
                [120, 125, 278] # index of word in this file
            ]
        } , { [ ] }  # and so on 
    ] 
}
'''
for folder_name in folder_names:
    file_names = natsorted(os.listdir( folder_name))
    for file_name in file_names:
        stuff = read_text_file( folder_name + "/" + file_name)
        final_token_list = normalizing(stuff)
        for pos, term in enumerate(final_token_list):
            term = stemmer.stem(term)
            if term in pos_index:
                pos_index[term][0] = pos_index[term][0] + 1
                if fileno in pos_index[term][1]:
                    pos_index[term][1][fileno].append(pos)
                else:
                    pos_index[term][1][fileno] = [pos]
            else:
                pos_index[term] = []
                pos_index[term].append(1)
                pos_index[term].append({})
                pos_index[term][1][fileno] = [pos]

        file_map[fileno] = folder_name + "/" + file_name
        fileno += 1

# user phares query
pharseQuery=input("Enter your pharse Query To search for it :")
pharseQuery = normalizing(pharseQuery)
Filtered_pharseQuery = [w for w in pharseQuery if not w in stop_words]

# return matched document
