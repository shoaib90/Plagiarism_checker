# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 01:59:24 2018

@author: soheb khan
"""

from collections import defaultdict
import math
import csv
import os
dictonary = defaultdict(list)

files= os.listdir('docs/')
tokens= []

for file in files:
    with open('docs/' + file, 'r') as f:
        split_f = f.read().split('\n\n')
        if len(split_f) > 1:
            for i, para in enumerate(split_f):
                with open('docs/' + file[:-4] + '_' + str(i) + '.txt', 'w') as w_f:
                    w_f.write(para)
                
    os.remove('docs/' + file)
    files= os.listdir('docs/')

class packet(object):
    filename = ""
    rep = 0
   
    # The class "constructor" - It's actually an initializer 
    def __init__(self):
        self.rep = 0
        self.fiename = ""
    
def filterToken(tokens):
    for a in tokens:
        if len(a)>0 and (a[len(a)-1] == '.' or a[len(a)-1] == ',' or a[len(a)-1] == '!' or a[len(a)-1] == '?') :
            tokens[tokens.index(a)]=a[0:len(a)-1]
            
    tokens = [a for a in tokens if a.isalpha() and len(a)>0]
    return tokens

def addToDict(tokens,name,text):
    global dictonary
    tokens = set(tokens)
    for i in tokens:
        obj = packet()
        rep = text.count(i)
        obj.filename = name
        obj.rep = rep
        dictonary[i].append(obj)
        
for i in files:
    filename='docs/'+i 
    file=open(filename,"r")
    text=file.read().lower()
    tokens=filterToken(text.split(' '))
    addToDict(tokens,i,text)

#tf-idf matrix
n = len(dictonary)
m = len(files)
matrix = [[0]*(m+1) for i in range(n)]
c = -1
for i in dictonary:
    c = c+1
    tf = 0
    idf = 0
    matrix[c][0] = i
    for j in range(1,m+1):
        for k in dictonary[i]:
            if(k.filename == files[j-1]):
                tf = k.rep
                idf = math.log(m/len(dictonary[i]))
                matrix[c][j]=round(tf*idf, 2)
                break
        else:
            matrix[c][j]=0

#converting to CSV file
csvfile = "matrix.csv"
matrix.append(files)
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in matrix:
        try:
            writer.writerow(val)  
        except:
            print(val[0])
            continue