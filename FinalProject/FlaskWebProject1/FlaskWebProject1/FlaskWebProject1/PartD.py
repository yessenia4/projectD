import time
import numpy as np
from FlaskWebProject1.PartA import *
from FlaskWebProject1.PartC import *

class SearchEngine:
    #variables
    ourCrawler = Crawler()
    Q = Parser()
    Processor = ProcessQ()
    termList = {}
    docList = {}

    def crawlIndex(self):
        print("Starting crawling and indexing...\n")
        startT = time.time()
        result = self.ourCrawler.startCrawl()
        endT = time.time()
        self.termList = result[0]
        self.docList = result[1]
        print("Finished crawling and indexing...\n")
        print("Crawling and Indexing Time: " + repr(endT - startT) + "\n")

    def getQTerms(self, trialQuery):
        termQList = []
        word = ''
        for char in trialQuery:
            if char == '(' or char == '*' or char == '+' or char == '!' or char == ')' or char == '"' or char == ' ':
                if word != '':
                    termQList.append(word)
                    word = ''
            else:
                word = word + char
        return termQList

    def sim(self,hitlist,qTerms):
        resultsRank = []
        totalDOC = len(self.docList)
        qLength = 0.00
        #get length of query
        for term in qTerms:
            qLength = qLength + math.pow(float(totalDOC / self.termList[term]['dfi']),2)
        qLength = math.sqrt(qLength)
        #get the value for each document to compare to query
        for doc in hitlist:
            resultsRank.append([doc,0]) #initialize
            index = resultsRank.index([doc,0])
            for term in qTerms:
                docResults = self.termList[term]['doclist']
                termFNorm = 0
                for document in docResults:
                    docId = document[0]
                    if docId == doc:
                        termFNorm = document[1]
                        break
                resultsRank[index][1] = resultsRank[index][1] + termFNorm
            docLength = self.docList.get(doc)['doc length']
            resultsRank[index][1] = resultsRank[index][1] / (docLength * qLength)
        #sort based on the similarity value
        resultsRank = sorted(resultsRank,key = lambda x:x[1], reverse= True)
        return resultsRank

    def getHitList(self,query):
        query = query.lower() + " end"
        queryTree = self.Q.p(query)
        #self.Q.print_tree_indented(queryTree,0)
        hitList = self.Processor.processTree(queryTree,self.termList,self.docList)
        #rank results
        rankedList = self.sim(hitList,self.getQTerms(query))
        #looks through the results....to get url
        hitListRanked = []
        for fileID in rankedList:
            d = self.docList.get(fileID[0])
            if (d != None):
                link = d['URL']
                #link = str.replace(link,'\\','/')
                hitListRanked.append([fileID[0],link])
        return hitListRanked

