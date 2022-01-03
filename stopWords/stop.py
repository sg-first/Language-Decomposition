import json
import stopWords.help as help

punctuation=['，','。','）','（','“','”','；','？','、']

def init(path):
    jsoncode=help.readTXT(path)
    global stoplist
    stoplist=json.loads(jsoncode)

def isStopWord(word):
    if word in punctuation:
        return True
    if word[0] in stoplist.keys():
        if word in stoplist[word[0]]:
            return True
    return False

init('stopWords/stopWordList(gen).txt')
