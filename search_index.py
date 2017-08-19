import os
from bs4 import BeautifulSoup
from llist import sllist, sllistnode
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import re
from operator import itemgetter
import unicodedata
index={}
#Problem to address-> global dictionary.
def extract(filename):
    with open(filename) as f:
        lines = f.readlines()
        content=''
        for line in lines:
            if len(line.split('\t'))>1:
                content=content+line.split('\t')[1]
        return content


def porter_stemmer(tokens):
    ps = PorterStemmer()
    stem_list=[]
    for w in tokens:
        if type(ps.stem(w)) is unicode:
            stem_list.append(unicodedata.normalize('NFKD',ps.stem(w)).encode('ascii','ignore'))
        else:
    	       stem_list.append(ps.stem(w))
    return stem_list

def sentence_boundary(filename):
    return nltk.sent_tokenize(unicode(extract(filename),"utf-8"))

def zipf(filename):
        frequency = {}
        words = re.findall(r'(\b[A-Za-z][a-z]{2,9}\b)',extract(filename))
        for word in words:
            count = frequency.get(word,0)
            frequency[word] = count + 1
        for key, value in reversed(sorted(frequency.items(), key = itemgetter(1))):
            return key, value

def tokenizer(filename):
    sent_text = nltk.sent_tokenize(unicode(extract(filename),"utf-8")) # this gives us a list of sentences
# now loop over each sentence and tokenize it separately
    for sentence in sent_text:
        tokenized_text = nltk.word_tokenize(sentence)
        tokens=[]
        for token in tokenized_text:
                tokens.append(unicodedata.normalize('NFKD', token).encode('ascii','ignore'))
        return tokens


def scrape_file(filename):
    file_content={}
    with open(filename) as f:
        content= f.read()
        soup=BeautifulSoup(content,"lxml")
    file_content['Document Name']=(content.split('<DOCNO>')[1]).split('</DOCNO>')[0]
    if len(content.split('<TITLE>'))>1:
            file_content['title']=(content.split('<TITLE>')[1]).split('</TITLE>')[0]
    file_content['text']=(content.split('<TEXT>')[1]).split('</TEXT>')[0]
    return file_content

def text_process(filename):
    #Returning as a tuple of stemmed text and document name.
    file_content=scrape_file(filename)
    text=file_content['text'].split()
    if 'title' in file_content.keys():
        text.extend(file_content['title'].split())
    return stemmer(text),file_content['Document Name']

def collect_dictionary_file(doc_tuple,index):
    for word in doc_tuple[0]:
        if word not in index.keys():
            index[word]=sllist([doc_tuple[1]])
        else:#word present in the index.
            if doc_tuple[1] not in index[word]:
                index[word].appendright(doc_tuple[1])
                index[word]=sllist(sorted(index[word]))
    return index
#Testing function. TBD.
def two_files():
    #print two_files()
    collect_dictionary_file('sample_file.txt')
    collect_dictionary_file('sample_file2.txt')
    return index

def search_query(words,index):
    if len(words)<=1:
        query_list=words.lower()
    else:
        query_list=(words.lower()).split()
    document_list=[]
    query_list=porter_stemmer(query_list)
    for word in query_list:
        if word in index.keys():
            document_list.append(index[word])
    return document_list
    #Consists of a list of sllists.

def print_result(link_list):
    final_list=[]
    for i in link_list:
        for value in i:
            if value not in final_list:
                final_list.append(value)
    return final_list
