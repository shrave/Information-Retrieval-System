from decimal import *
import sys

f=open('page-rank_data.txt','r')
nodes=f.readlines()
matrix_size=len(nodes)
page_dict={}
for i in nodes:
    pages=i.split()
    pages = filter(None, pages)
    if pages:
        key=pages[0]
        del pages[0]
        page_dict[key]=pages


def total_links(node):
    pages_pointing = []
    for pages in page_dict.values():
        for page in pages:
            if node == page:
                pages_pointing.append(page_dict.keys()[page_dict.values().index(pages)])
    return pages_pointing

#Where page_dict is a dictionary consisting of a page and the links going out from it.
def page_rank(page_dict):
    dict1 = {}
    dict2 = {}
    n = len(page_dict)
    getcontext().prec = 20
    initial = Decimal(100)/Decimal(n)
    print str(initial)
    for i in page_dict.keys():
        dict1[i] = initial
        dict2[i] = initial
    damp = 0.8
    ep = Decimal(sys.float_info.epsilon)

    ite = 0
    while(1):
        for i in page_dict.keys():
            sum = 0
            if total_links(i):
                for node in total_links(i):
                    sum = sum + Decimal(dict1[node])/Decimal(len(page_dict[node]))
                    dict2[i] = (Decimal(1) - Decimal(damp))/Decimal(n) + Decimal(damp) * sum

        for i in page_dict.keys():
            sum = 0
            if total_links(i):
                for node in total_links(i):
                    sum = sum + Decimal(dict2[node])/Decimal(len(page_dict[node]))
                    dict1[i] = (Decimal(1) - Decimal(damp))/Decimal(n) + Decimal(damp) * sum
        ite = ite + 1
        k = 0
        for i in page_dict.keys():
            if abs(dict1[i] - dict2[i]) < ep:
                break
            k = k + 1

        if(k < n):
    #        print ite
    #        print k
            break
