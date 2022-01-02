import gensim
import tag

tag.loadWcModel('word2vec/word2vec_wx')
print('loaded')

while True:
    word=input()
    try:
        res=tag.model.most_similar(word)
    except:
        print('未找到')
        continue
    print(res)
