import gensim
import tag

tag.loadWcModel('word2vec/word2vec_wx')
print('loaded')

tag.setWordTag('国外','优越',7)
tag.setWordTag('国内','优越',6)
tag.setWordTag('异域','文艺',7)
tag.setWordTag('风情','文艺',6.5)
tag.setWordTag('体会','文艺',6)
tag.setWordTag('体会','严肃',6)
tag.setWordTag('探索','严肃',6)

tag.setWordTag('老家','优越',-6)
tag.setWordTag('概念','严肃',7)
tag.setWordTag('模糊','严肃',6)
tag.setWordTag('模糊','悲伤',2.5)
tag.setWordTag('绝望','悲伤',8)
tag.setWordTag('绝望','严肃',7)
tag.setWordTag('绝望','文艺',7)
tag.setWordTag('逃避','悲伤',7)
tag.setWordTag('逃避','严肃',7)
tag.setWordTag('逃避','文艺',7)
tag.setWordTag('面对','严肃',2)
tag.setWordTag('面对','文艺',2)

tag.setWordTag('扮演','严肃',3)
tag.setWordTag('人格','严肃',4)
tag.setWordTag('人格','文艺',4)
tag.setWordTag('分裂','严肃',4)
tag.setWordTag('分裂','文艺',5)
tag.setWordTag('分裂','悲伤',7.5)

tag.setWordTag('远','悲伤',2)
tag.setWordTag('近','悲伤',0)

tag.saveWordTag('tag.pk')

import jieba
content='我想，小时候总想往国外跑 一是想看看异域风景（虽然现在也才体会到别说中国 后边的小山坡就有够我探索的了）  另一是老家被毁 各种那啥一并发生 本身对家（归属地）的概念已经模糊/绝望了 所能想到的只有逃避（中二扮演人格分裂也是） 而国外（尤其美国）是我所能逃到的离这最远的地方'
segList = jieba.cut(content, cut_all=False)

sumDimtag=tag.dimTag()
segListLen=0
for w in segList:
    if w in tag.word2Dimtag.keys():
        dimtag=tag.word2Dimtag[w]
        print(w,dimtag.dim2val)
        sumDimtag=sumDimtag.addTag(dimtag)
        segListLen+=1
sumDimtag.avg(segListLen)
print(sumDimtag.dim2val)
