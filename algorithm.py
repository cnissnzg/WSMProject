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
                    termList.append(a.lower())
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
                
## xxx && yyy || !! ( zzz && ttt )
def booleanQuery(seq):
    n = len(seq)
    if n == 0 :
        return set()
    if n == 1:
        res = set()
        idx = termDict[seq[0]]
        for idxItem in invIdxs[idx]:
            if idxItem['docId'] not in res:
                res.add(idxItem['docId'])
        return res
    
    if seq[0] == '(' and seq[-1] == ')':
        return booleanQuery(seq[1:-1])
    inStack = 0
    for i in range(n):
        if seq[i] == '(':
            inStack += 1
        elif seq[i] == ')':
            inStack -= 1
        elif inStack == 0:
            if seq[i] == "&&":
                resLeft = booleanQuery(seq[:i])
                resRight = booleanQuery(seq[i+1:])
                return resLeft.intersection(resRight)
            elif seq[i] == "||":
                resLeft = booleanQuery(seq[:i])
                resRight = booleanQuery(seq[i+1:])
                return resLeft.union(resRight)
    if seq[0] == "!!":
        res = set()
        resRight = booleanQuery(seq[1:])
        for i in range(nTerm):
            if i not in resRight:
                res.add(i)

if __name__ == "__main__":
    init()