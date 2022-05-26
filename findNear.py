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

tag.loadWordTag('love2.pk')

def findNeighborhood(word:str, wordTag:tag.dimTag, targetTag:tag.dimTag):
    simWord = tag.model.most_similar(word)

    minLossVal=None
    minNewTag=None
    minWord=None
    for w, sim in simWord:
        try:
            newTag = tag.word2Dimtag[w]
        except KeyError:
            continue
        diffTag = newTag.diffTag(targetTag)
        print(w, diffTag.dim2val)
        oldDiffTag = wordTag.diffTag(targetTag)
        lossVal = diffTag.absSum()
        oldLossVal = oldDiffTag.absSum()
        if oldLossVal<=lossVal:
            continue

        if minLossVal is None or lossVal<minLossVal:
            minLossVal=lossVal
            minNewTag=newTag
            minWord=w

    if not minWord is None:
        print('result:',minWord,minNewTag)
        findNeighborhood(minWord,minNewTag,targetTag)

word='可爱'
dimtag=tag.word2Dimtag[word] # 尝试变它
targetTag=tag.dimTag()
targetTag.dim2val={'发展关系':10,'内在':10}
findNeighborhood(word,dimtag,targetTag)