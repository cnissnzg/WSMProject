import jieba
import re
import dataloader

partList = ["content","title"]
docs = []
termList = []
nTerm = 0
invIdxs = dict()
termDict = dict()
idxDict = dict()

def init(path='data'):
    docs = dataloader.getDocs(path)
    nTerm = 0
    for i in range(len(docs)):
        print('Building index from doc {} in {}'.format(i,len(docs)))
        '''
        if i == 10:
            print(invIdxs)
            print(termDict)
            print(idxDict)
            exit(0)
        '''
        doc = docs[i]
        for part in partList:
            segList = jieba.cut_for_search(doc[part])
            termList = []
            for seg in segList:     
                a=re.sub(r'[\W]','',seg)
                if a != '':
                    termList.append(a)
            for j in range(len(termList)):
                term = termList[j]
                if term not in termDict:
                    termDict[term] = nTerm
                    idxDict[nTerm] = term
                    invIdxs[nTerm] = []
                    nTerm+=1
                idx = termDict[term]
                invIdxs[idx].append({
                    'docId' : i,
                    'type' : part,
                    'pos' : j
                })

if __name__ == "__main__":
    init()