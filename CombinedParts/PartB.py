import os, glob, nltk, string, re
import math
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


class Indexer:

    wordIndex = {}
    docList = {}
    
    def getIndexes(self):
        self.updateDF_id()
        self.normal()
        return [self.wordIndex,self.docList]
    
    def helper_I(self, wordText, text, docID, fileName):
        self.docList[docID] = {'doc length': 0.0, 'URL': fileName, 'max freq': 0}
        for word in wordText:
            if(self.wordIndex.get(word) == None):
                Tdoclist = []
                listPositions = [s.start() for s in re.finditer(word,text)]
                tf = float(len(listPositions))
                if(tf > self.docList[docID]['max freq']):
                    self.docList[docID]['max freq'] = tf
                Tdoclist.append([docID, tf, listPositions])
                self.wordIndex[word] = {'dfi': 1, 'doclist': Tdoclist}
            else:
                x = len(self.wordIndex[word]['doclist']) - 1
                if(self.wordIndex[word]['doclist'][x][0] != docID):
                    listPositions = [s.start() for s in re.finditer(word,text)]
                    tf = float(len(listPositions))
                    if(tf > self.docList[docID]['max freq']):
                        self.docList[docID]['max freq'] = tf
                    self.wordIndex[word]['doclist'].append([docID, tf, listPositions])
    
    def updateDF_id(self):
        for word in self.wordIndex:
            self.wordIndex[word]['dfi'] = int(len(self.wordIndex[word]['doclist']))
            
    def normal(self):
        totalDOC = len(self.docList)
        for word in self.wordIndex:
           x = float(totalDOC / self.wordIndex[word]['dfi'])
           for doc in self.wordIndex[word]['doclist']:
               doc[1] = float(doc[1]/self.docList[doc[0]]['max freq'])
               self.docList[doc[0]]['doc length'] = self.docList[doc[0]]['doc length'] + math.pow((doc[1] * x),2)
        for doc in self.docList:
            self.docList[doc]['doc length'] = math.pow(self.docList[doc]['doc length'],0.5)
    
    def printIndex(self):
        wordIndexFile = open('wordIndex.txt','+a')
        for key,word in self.wordIndex.items():
            wordIndexFile.write(str(key))
            wordIndexFile.write('\n')
            for attribute,value in word.items():
                wordIndexFile.write('{} : {}'.format(attribute,value))
                wordIndexFile.write('\n')
        docIndexFile = open('docIndex.txt','+a')
        for key,doc in self.docList.items():
            docIndexFile.write(str(key))
            docIndexFile.write('\n')
            for attribute,value in doc.items():
                docIndexFile.write('{} : {}'.format(attribute,value))
                docIndexFile.write('\n')

