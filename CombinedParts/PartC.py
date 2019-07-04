import os, glob, nltk, string, re, math
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from PartB import *


class Crawler:
    ourIndex = Indexer()

    def tokenizer(self, html_doc, originalPath):
        soup = BeautifulSoup(html_doc, 'html.parser')
        text = soup.get_text()
        lines = text.split('\n')
        noGoogleLines = []
        for line in lines:
            if 'google_ad' not in line:
                noGoogleLines.append(line)
            text = '\n'.join(noGoogleLines)
        #preprocessing
        text = text.lower()
        tokenizer = RegexpTokenizer(r'\w+')
        wordsText = tokenizer.tokenize(text)    #separates the words based on space and punctuation
        en_stops = set(stopwords.words('english'))
        wordsText = [word for word in wordsText if word not in en_stops]
        #get all the links in the html file...
        links = []
        for link in soup.find_all('a'):
            rawLink = link.get('href')
            if rawLink != None:
                if rawLink.endswith('.html'):
                    links.append([originalPath,link.get('href'),html_doc.name])
        return [text,wordsText,links]

    def obtainPath(self,html_doc_Name):
        paths = html_doc_Name.split('\\')
        p = '\\'.join(paths[:-1]) + '\\'
        name = '\\'.join(paths)
        paths = paths[:-1]
        return [paths,p,name]

    def crawl(self,html_doc, visitedLinkList,originalDir):
        notFoundFiles = []
        results = self.tokenizer(html_doc,originalDir)
        allLinks = results[2]
        visitedLinkList.append(str(originalDir + html_doc.name))
        while allLinks != []:
            link = allLinks[0][1]
            if allLinks[0][0] == '\\':
                originalPath = ''
            else:
                originalPath = allLinks[0][0]
            allLinks = allLinks[1:]
            fullPath = os.path.join(originalPath,link)
            if fullPath.endswith('.html'):
                try:
                    f2 = open(fullPath, encoding="utf8", errors='ignore')
                except FileNotFoundError:
                    notFoundFiles.append(fullPath)
                f2Name = os.path.realpath(f2.name)
                if f2Name not in visitedLinkList:
                    #print(f2Name)
                    visitedLinkList.append(f2Name)
                    pathResults = self.obtainPath(f2Name)
                    results2 = self.tokenizer(f2,pathResults[1])
                    indexDoc = visitedLinkList.index(f2Name)
                    self.ourIndex.helper_I(results2[1],results2[0],indexDoc,f2Name)  #updating index as we crawl
                    allLinks = allLinks + results2[2]   #update links that need to be visited
            else:
                visitedLinkList.append(link)
        print("Links Not Found: " + repr(len(notFoundFiles)))
        return visitedLinkList


    def startCrawl(self):
        l = open("rhf\index.html")
        visitedLinks = self.crawl(l,[],'C:\\Users\\Rodriguez\\source\\repos\\PythonPartAB\\PythonPartAB\\rhf')
        print("Visited Links: " + repr(len(visitedLinks)))
        indexes = self.ourIndex.getIndexes()
        return indexes