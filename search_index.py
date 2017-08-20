import os
from bs4 import BeautifulSoup
from llist import sllist, sllistnode
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import re
import html2text
from operator import itemgetter
import unicodedata
import pickle

index={}
word_frequency = {}
stopwords = ['a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst','amount', 'an', 'and', 'another', 'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around', 'as', 'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bill', 'both', 'bottom', 'but', 'by', 'call', 'can', 'cannot', "can't", 'co', 'con', 'could', "couldn't", 'cry', 'de', 'describe', 'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg.', 'eight', 'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few', 'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former', 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get', 'give', 'go', 'had', 'has', "hasn't", 'have', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', 'hundred', 'i.e.', 'if', 'in', 'inc', 'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never', 'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'the', 'their', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third', 'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself', 'yourselves']
#319 stopwords
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

def clear_tags(file_handle):
    h = html2text.HTML2Text()
    file_content = h.handle(file_handle.read())
    return file_content

def collect_content(root,file_name):
    
    """ for removes the XML tags from file_name and returns content """

    file_path = os.path.join(root, file_name)
    current_file = open(file_path,"r")
    file_content = clear_tags(current_file)
    current_file.close()
    return file_content

def filter_valid_tokens(token_list):
    reg_ex = """([-!$%^&*\(\)_+|~=`{}\[\]:";'<>?,.\/])+"""
    valid_tokens = filter(lambda x: not re.match(reg_ex,x), tokens)
    return valid_tokens

def modify_word_frequency_per_document(valid_token_list,doc_no):
    token_list = porter_stemmer(valid_token_list)

    for token in token_list:
        if not word_frequency.has_key(token):
            word_frequency[token] = {doc_no:1}
        else:
            if not word_frequency[token].has_key(doc_no):
                word_frequency[token][doc_no] = 1
            else:
                word_frequency[token][doc_no] += 1

def dump_structure(structure,pickle_file):
    file_handle = open(pickle_file,"wb")
    pickle.dump(structure, file_handle, -1)
    file_handle.close()

def find_word(final_index,word): 
    if final_index < 0 or final_index >= len(stopwords):
        return -1

    mid = final_index/2

    if stopwords[mid] == word:
        return mid
    else if stopwords[mid] < word:
        final_index = mid + 1
        find_word(final_index, word)
    else:
        final_index = mid - 1
        find_word(final_index, word)

def is_stop_word(word):
    if find_word(len(stopwords)-1, word) == -1:
        return False
    else:
        return True

def filter_out_stop_words(raw_tokens):
    return filter(lambda x: not is_stop_word(x), raw_tokens)


