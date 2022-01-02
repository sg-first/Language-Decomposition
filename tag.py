from gensim.models.keyedvectors import KeyedVectors
from gensim.models import Word2Vec
import math
import copy
import pickle

class dimTag:
    def __init__(self):
        self.dim2val={}

    def add(self,dim,val):
        if not dim in self.dim2val.keys():
            self.dim2val[dim]=0
        self.dim2val[dim]+=val

    def get(self,dim):
        return self.dim2val[dim]

    def addTag(self,tag):
        retTag=copy.copy(self)

        for dim,val in tag.dim2val.items():
            print(dim,val)
            retTag.add(dim,val)

        return retTag

    def avg(self,len):
        for dim,_ in self.dim2val.items():
            self.dim2val[dim]/=len

model=None

def loadWcModel(path):
    global model
    model = Word2Vec.load(path)

def loadKvModel(path):
    global model
    model = KeyedVectors.load_word2vec_format(path, binary=False)

word2Dimtag={}

def saveWordTag(path):
    file = open(path, 'wb')
    pickle.dump(word2Dimtag, file)

def loadWordTag(path):
    file = open(path, 'rb')
    global word2Dimtag
    word2Dimtag=pickle.load(file)

def createWordDimtag(word):
    if not word in word2Dimtag.keys():
        word2Dimtag[word]=dimTag()

def setWordTag(word,dim,val):
    createWordDimtag(word)
    word2Dimtag[word].add(dim,val)

    def prop(word,dim,val,visitedWord,layer=0):
        if layer==901 or math.fabs(val)<0.1:
            return
        else:
            simWord=model.most_similar(word)
            for w,sim in simWord:
                if not w in visitedWord:
                    createWordDimtag(w)
                    print(dim,val,'to',w)
                    delta=val*sim
                    word2Dimtag[w].add(dim,delta)
                    visitedWord.add(w)
                    prop(w,dim,delta,visitedWord,layer+1)
    prop(word,dim,val,set())

def getAnalogy(pair1, pair2, word1):
    return model.most_similar(positive=[pair2, word1], negative=[pair1])
# print(getAnalogy('北京','中国','东京'))