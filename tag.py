from gensim.models.keyedvectors import KeyedVectors
from gensim.models import Word2Vec
import math
import copy
import pickle
import numpy as np
import copy

class dimTag:
    def __init__(self):
        self.dim2val={}

    def add(self,dim:str,val):
        if not dim in self.dim2val.keys():
            self.dim2val[dim]=0
        self.dim2val[dim]+=val

    def get(self,dim:str) -> float:
        if not dim in self.dim2val.keys():
            self.dim2val[dim]=0
        return self.dim2val[dim]

    def addTag(self,tag):
        retTag=copy.copy(self)

        for dim,val in tag.dim2val.items():
            retTag.add(dim,val)

        return retTag

    def diffTag(self,tag):
        ret=dimTag()
        ret.dim2val=copy.copy(tag.dim2val)
        for dim, val in tag.dim2val.items():
            ret.dim2val[dim] = val - self.get(dim)
        return ret

    def absSum(self):
        s=0
        for _, val in self.dim2val.items():
           s+=abs(val)
        return s

    def avg(self,len) -> float:
        for dim,_ in self.dim2val.items():
            self.dim2val[dim]/=len

    def norm(self):
        valList=list(self.dim2val.values())
        std=np.std(valList)

        for dim, _ in self.dim2val.items():
            self.dim2val[dim]=(self.dim2val[dim])/std


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

def setWordTag(word:str, dim:str, val, isAdd=True):
    createWordDimtag(word)
    if not isAdd:
        val=val-word2Dimtag[word].get(dim) #fix:限制递归层数？

    word2Dimtag[word].add(dim, val)

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

    visitedWord=set()
    visitedWord.add(word)
    prop(word,dim,val,visitedWord)

def getAnalogy(pair1, pair2, word1):
    return model.most_similar(positive=[pair2, word1], negative=[pair1])
# print(getAnalogy('北京','中国','东京'))

if __name__=='__main__':
    loadWcModel('word2vec/word2vec_wx')
    loadWordTag('tag.pk')
    print('loaded')
    while True:
        word=input('word:')
        if word=='save':
            saveWordTag('tag2.pk')
            print('saved')
            continue
        elif word=='query':
            word = input('word:')
            print(word2Dimtag[word].dim2val)
        else:
            dim=input('dim:')
            val=input('val:')
            setWordTag(word,dim,float(val),False)
            print('finished')
