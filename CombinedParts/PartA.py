from nltk.tokenize import *
from collections import Counter

class Tree:
    def __init__(self, cargo, left=None, right=None):
        self.cargo = cargo
        self.left  = left
        self.right = right
    def __str__(self):
        return str(self.cargo)
    def total(tree):
        if tree == None: return 0
        return total(tree.left) + total(tree.right) + tree.cargo

class Parser:
    def p(self, fpexp):
        #fplist = fpexp.split()  #may be able to work with spaces instead of plus sign if create a split function
        fplist =  self.splitQuery(fpexp)
        #print(fplist)
        tree = self.get_sum(fplist)
        return tree
    def get_token(self, token_list, expected):
        if token_list[0] == expected:
            del token_list[0]
            return True
        else:
            return False
    def get_word(self, token_list):
        if self.get_token(token_list, '('):
            x = self.get_sum(token_list)         # get the subexpression
            self.get_token(token_list, ')')      # remove the closing parenthesis
            return x
        elif self.get_token(token_list, '!('):
            x = self.get_sum(token_list)
            self.get_token(token_list, ')')      # remove the closing parenthesis
            return Tree ('!',x,None)
        else:
            x = token_list[0]
            #if type(x) != type(0): return None
            token_list[0:1] = []
            return Tree (x, None, None)
    def get_not(self, token_list):
        #a = self.get_word(token_list)
        if self.get_token(token_list, '!'):
            a = self.get_word(token_list)
            return Tree ('!',a, None)
        else:
            return self.get_word(token_list)
    def get_product(self, token_list):
        a = self.get_not(token_list)
        if self.get_token(token_list, '*'):
            b = self.get_product(token_list) 
            return Tree ('*', a, b)
        else:
            return a
    def get_sum(self,token_list):
        a = self.get_product(token_list)
        if self.get_token(token_list, '+'):
            b = self.get_sum(token_list)
            return Tree ('+', a, b)
        else:
            return a
    def print_tree_indented(self,tree, level=0):
        if tree == None: return
        self.print_tree_indented(tree.right, level+1)
        print('  ' * level + str(tree.cargo))
        self.print_tree_indented(tree.left, level+1)
    def splitQuery(self,trialQuery):
        indexCount = 0
        tokenList = []
        quotesFound = False
        word = ''
        for char in trialQuery:
            if(quotesFound == False):
                if char == '(' or char == '*' or char == '+' or char == '!' or char == ')':
                    if word != '':
                        tokenList.append(word)
                        word = ''
                    tokenList.append(char)
                elif char == '"':
                    if word != '':
                        tokenList.append(word)
                        word = ''
                    tokenList.append(char)
                    indexCount = tokenList.index(char)
                    quotesFound = True
                elif char == ' ':
                    if word != '':
                        tokenList.append(word)
                        word = ''
                else:
                    word = word + char
            else:
                if char != '"':
                    tokenList[indexCount] = tokenList[indexCount] + char
                else:
                    tokenList[indexCount] = tokenList[indexCount] + char
                    quotesFound = False
        if word != '':
            tokenList.append(word)
            word = ''
        return tokenList

class ProcessQ:
    def processTree(self, tree, termList, docLists):
        if(tree.cargo == '+'):
            return list(self.processOR(tree.right, tree.left, termList, docLists))
        elif (tree.cargo == '*'):
            return list(self.processAND(tree.right, tree.left, termList, docLists))
        elif (tree.cargo == '!'):
            return list(self.processNOT(tree.left, termList, docLists))
        else:
            return list(self.processTerm(tree.cargo, termList, docLists))

    def processOR(self, rightTree, leftTree, termList, docLists):
        #print(repr(rightTree.cargo) + " OR " + repr(leftTree.cargo))
        rightResults = self.processTree(rightTree, termList, docLists)
        leftResults = self.processTree(leftTree, termList, docLists)
        
        results = leftResults + rightResults
        results = list(dict.fromkeys(results))

        return results

    def processAND(self, rightTree, leftTree, termList, docLists):
        #print(repr(rightTree.cargo) + " AND " + repr(leftTree.cargo))
        rightResults = self.processTree(rightTree, termList, docLists)
        leftResults = self.processTree(leftTree, termList, docLists)

        return list(set(rightResults) & set(leftResults))

    def processTerm(self, term, termList, docLists):
        #check if first character is "!"
        if term[0] is '!':
            return self.processNotTerm(term, termList, docLists)
        if term[0] is '"':
            return self.processQuotes(term, termList, docLists)
        results = []
        r = termList.get(term)
        if (r != None):
            temp = r['doclist']
            results = results + [i[0] for i in temp]
        return results

    def processNotTerm(self, term, termList, docLists):
        temp = [i[0] for i in docLists]
        #temp = list(chain(*[list((sub[0], 0)) for sub in docLists])) 
        term = term[1:] #gets rid of the exclamation mark
        r = termList.get(term)
        if (r != None):
            docResults = r['doclist']
            docIndexes = [i[0] for i in docResults]
            for index in docIndexes:
                temp.pop(index)
            results = list(temp)

        return results

    def processNOT(self, tree, termList, docLists):
        results = [i[0] for i in docLists]
        #results = list(chain(*[list((sub[0], 0)) for sub in docLists])) 
        notResults = self.processTree(tree, termList, docLists)

        return list(set(results) - set(notResults))

    def processQuotes(self, text, termList, docLists):
        tokenizer = RegexpTokenizer(r'\w+')
        text = text[1:-1]
        terms = tokenizer.tokenize(text)    #separates the words based on space and punctuation

        tempResults = []
        index = 0
        for index in range(len(terms)-1):
            term1Results = self.processTerm(terms[index], termList, docLists)
            term2Results = self.processTerm(terms[index+1], termList, docLists)
            sameResults = list(set(term1Results) & set(term2Results))
            for document in sameResults:
                docResults = termList[terms[index]]['doclist']
                term1Pos = docResults[docResults[:,0]==document][2]
                docResults = termList[terms[index+1]]['doclist']
                term2Pos = docResults[docResults[:,0]==document][2]
                for position in term1Pos:
                    startTerm2 = position + len(terms[index]) + 1
                    for position2 in term2Pos:
                        if position2 == startTerm2:
                            tempResults.append(document)
                            break
                    if document in tempResults: #checking if need to check additional positions/postings
                        break
        counts = Counter(tempResults)
        results = [value for value, count in counts.items() if count == len(terms)-1]
        return results