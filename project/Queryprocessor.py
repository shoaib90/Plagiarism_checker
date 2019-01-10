# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 01:01:41 2018

@author: soheb khan
"""

import csv
import math

matrix = []
doc=[]
filestore=[]
query=["New Text Document.txt"]


#print(matrix)


def filterToken(tokens):
    for a in tokens:
        if len(a)>0 and (a[len(a)-1] == '.' or a[len(a)-1] == ',' or a[len(a)-1] == '!' or a[len(a)-1] == '?') :
            tokens[tokens.index(a)]=a[0:len(a)-1]
            
    tokens = [a for a in tokens if a.isalpha() and len(a)>0]
    return tokens

def openfile():
    global matrix
    with open('matrix.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            matrix.append(row)

        csvFile.close()


def column(mat, i):
    return [row[i] for row in mat]

def retrieveDocs(query,m,files,n):
    global doc,matrix
    doc.append(column(matrix, 0))
    for k in query:
        for i in range(n):
            if(matrix[i][0] == k):
                for j in range(1,m):
                    if (float(matrix[i][j])>0) and files[j - 1][0] not in filestore:
                        doc.append(column(matrix, j))
                        filestore.append([files[j-1],0])

for i in query:
    filename=i 
    file=open(filename,"r")
    text=file.read()


openfile()
n = len(matrix)
files = matrix[n-1]
matrix=matrix[0:n-1]
n = n-1
m = len(matrix[0])-1
query = filterToken(text.lower().split(' '))
#query = filterToken(text.lower().split(' '))
doc=[]
retrieveDocs(query,m,files,n)


#for i in range(len(filestore)):
#   filestore.append(0)
   
#queryArray = []
queryAmp = 0
for i in doc[1]:
    #queryArray.append(1)
    queryAmp = queryAmp + float(i)
    #else:
     #   queryArray.append(0)

queryAmp = math.sqrt(queryAmp)

#cosine similarity
for i in range(1,len(doc)):
    sum = 0
    amp = 0
    for j in range(len(doc[i])):
        amp = amp + float(doc[i][j])**2
        if doc[0][j] in query:
            sum = sum + float(doc[i][j])
    amp = math.sqrt(amp)
    filestore[i-1][1] = sum/(amp*queryAmp)


#Sorting and filtering based on cosine score
n = len(filestore) 
for i in range(n):
    for j in range(0, n-i-1):
            if filestore[j][1] < filestore[j+1][1] :
                filestore[j], filestore[j+1] = filestore[j+1], filestore[j]
                

temp= filestore[0]
for i in filestore:
    if i[1]>temp[1]:
        temp=i

#print('123')
print("Plagiarism: {}% From file: {}".format(temp[1]*100,temp[0]))

print("Plagiarism: ",temp[1]*100,"% From file:",temp[0])