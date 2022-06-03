import jieba
import re
import dataloader
import math

partList = ["content","title"]
docs = []
termList = []
nTerm = 0
invIdxs = dict()
termDict = dict()
idxDict = dict()
termDF = dict()
invDateIdxs = list()

def getTermList(text):
    segList = jieba.cut_for_search(text)
    termList = []
    for seg in segList:     
        a=re.sub(r'[\W]','',seg)
        if a != '':
            termList.append(a.lower())
    return termList

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
        invDateIdxs.append([doc['parseTime'],i])
        for part in partList:
            termList = getTermList(doc[part])
            termCntSet = set()
            for j in range(len(termList)):
                term = termList[j]
                if term not in termDict:
                    termDict[term] = nTerm
                    idxDict[nTerm] = term
                    invIdxs[nTerm] = []
                    termDF[nTerm] = 0
                    nTerm+=1
                idx = termDict[term]
                invIdxs[idx].append({
                    'docId' : i,
                    'type' : part,
                    'pos' : j
                })
                if idx not in termCntSet:
                    termDF[idx] += 1
                    termCntSet.add(idx)
            termCntSet.clear()
    invDateIdxs.sort(key=lambda ele:ele[0])
        
                
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
                
'''
bound: oldest article time
source: article source
'''
def specificQuery(bound,source=None):
    l,r,mid,ans = 0,len(docs)-1,-1,-1
    while l <= r:
        mid = (l + r) // 2
        if(docs[mid]['parseTime'] < bound):
            l = mid + 1
        else:
            ans = mid
            r = mid - 1
    ret = set()
    if ans == -1:
        return ret
    else:
        for i in range(ans,len(docs)):
            if source == None or docs[i]['source'] == source:
                ret.add(i)
        return ret

'''
query: query text
topk: number of top results to return
'''
def rankedSearch(query,topk):
    termList = getTermList(query)
    res = []
    nDocs = len(docs)
    topk = min(topk,nDocs)
    for i in range(nDocs):
        score = 0.0
        for term in termList:
            idx = termDict[term]
            termIDF = math.log2(nDocs/(1+termDF[idx]))
            termTF = 0
            for invIdx in invIdxs[idx]:
                if invIdx['docId'] ==  i:
                    termTF += 1
            score += termTF*termIDF
        res.append({
            'id' : i,
            'score' : score
        })
    res.sort(key=lambda ele:ele['score'])
    retSet = set()
    for i in range(topk):
        retSet.add(res[i]['id'])
    return retSet
    

if __name__ == "__main__":
    init()
    print(invDateIdxs)