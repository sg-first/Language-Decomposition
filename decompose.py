import gensim
import tag
import stopWords.stop

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

    def avg(self,len):
        for dim,_ in self.dim2val.items():
            self.dim2val[dim]/=len

    def norm(self):
        valList=list(self.dim2val.values())
        std=np.std(valList)

        for dim, _ in self.dim2val.items():
            self.dim2val[dim]=(self.dim2val[dim])/std

tag.loadWcModel('word2vec/word2vec_wx')
print('loaded')

tag.loadWordTag('love2.pk')

import jieba
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False

def decompose(content):
    segList = jieba.cut(content, cut_all=False)

    sumDimtag=tag.dimTag()
    segListLen=0
    for w in segList:
        if (not stopWords.stop.isStopWord(w)) and w in tag.word2Dimtag.keys():
            dimtag=tag.word2Dimtag[w]
            print(w,dimtag.dim2val)
            sumDimtag=sumDimtag.addTag(dimtag)
            segListLen+=1
    sumDimtag.norm()
    print(content)
    print(sumDimtag.dim2val)
    plt.bar(sumDimtag.dim2val.keys(), sumDimtag.dim2val.values())
    plt.show()

decompose('我很崇拜你这种闪闪发光的人')

while True:
    content=input()
    decompose(content)
