import copy
import stopWords.stop
import tag

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

tag.loadWcModel('word2vec/word2vec_wx')
print('loaded')

tag.loadWordTag('tag.pk')

import jieba.posseg as psg

def getFlag(word):
    seg = psg.cut(word)
    for word, flag in seg:
        return flag

content='但我还寻求新的可能性，所以我已经略有些社牛，可以大方地向任何有兴趣的人搭话了。不过这都没有给人讲题好玩。我发现研究透一题的思想方法时，再给人别讲解到大彻大悟的时候，信心树立起来，心情是极好的。讲着讲着就思路更顺了，语言组织更流畅了，人也不困了。我想多寻找这样的感觉。我迫切地想提升思考能力'
targetTag=tag.dimTag()
targetTag.dim2val={'悲伤':10}

def findNeighborhood(word:str, flag:str, wordTag:tag.dimTag, targetTag:tag.dimTag):
    simWord = tag.model.most_similar(word)

    minLossVal=None
    minNewTag=None
    minWord=None
    for w, sim in simWord:
        if getFlag(w)!=flag:
            continue
        try:
            newTag = tag.word2Dimtag[w]
        except KeyError:
            continue
        diffTag = newTag.diffTag(targetTag)
        oldDiffTag = wordTag.diffTag(targetTag)
        lossVal = diffTag.absSum()
        oldLossVal = oldDiffTag.absSum()
        if oldLossVal<=lossVal:
            continue

        if minLossVal is None or lossVal<minLossVal:
            minLossVal=lossVal
            minNewTag=newTag
            minWord=w

    return minNewTag, minWord

def rewrite(content,targetTag):
    segList = psg.cut(content)
    newContent = ''

    for w, flag in segList:
        if stopWords.stop.isStopWord(w):
            newContent += w
        elif w in tag.word2Dimtag.keys():
            dimtag=tag.word2Dimtag[w] # 尝试变它
            newTag, newWord = findNeighborhood(w,flag,dimtag,targetTag)
            if newTag is None:
                newContent += w
            else:
                print(w, 'to', newWord)
                print(dimtag.dim2val)
                print(newTag.dim2val)
                newContent+=newWord
        else:
            newContent += w
    print(content)
    print(newContent)

rewrite(content,targetTag)