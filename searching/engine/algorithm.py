import jieba
import re
import datetime
from searching.engine import dataloader
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
class tools():
    partList = ["content","title"]
    docs = []
    termList = []
    nTerm = 0
    invIdxs = dict()
    termDict = dict()
    idxDict = dict()
    termDF = dict()
    invDateIdxs = list()
    nLabel = 0

    def getTermList(self, text):
        segList = jieba.cut_for_search(text)
        termList = []
        for seg in segList:     
            a=re.sub(r'[\W]','',seg)
            if a != '':
                termList.append(a.lower())
        return termList

    def clustering(self, docs):
        words=[]
        for i in range(len(docs)):
            doc=docs[i]
            word=doc['title']
            words.append(word)
        vect = CountVectorizer()
        x = vect.fit_transform(words)
        x = x.toarray()
        words_name = vect.get_feature_names()
        df = pd.DataFrame(x, columns=words_name)
        df_cs = cosine_similarity(df)
        kms_cs = KMeans(n_clusters=4, random_state=0)
        label_kms_cs = kms_cs.fit_predict(df_cs)
        return label_kms_cs

    def init(self, path='data'):
        self.docs = dataloader.getDocs(path)
        self.nTerm = 0
        for i in range(len(self.docs)):
            print('Building index from doc {} in {}'.format(i,len(self.docs)))
            '''
            if i == 10:
                print(invIdxs)
                print(termDict)
                print(idxDict)
                exit(0)
            '''
            doc = self.docs[i]
            self.invDateIdxs.append([doc['parseTime'],i])
            for part in self.partList:
                termList = self.getTermList(doc[part])
                termCntSet = set()
                for j in range(len(termList)):
                    term = termList[j]
                    if term not in self.termDict:
                        self.termDict[term] = self.nTerm
                        self.idxDict[self.nTerm] = term
                        self.invIdxs[self.nTerm] = []
                        self.termDF[self.nTerm] = 0
                        self.nTerm+=1
                    idx = self.termDict[term]
                    self.invIdxs[idx].append({
                        'docId' : i,
                        'type' : part,
                        'pos' : j
                    })
                    if idx not in termCntSet:
                        self.termDF[idx] += 1
                        termCntSet.add(idx)
                termCntSet.clear()
        self.invDateIdxs.sort(key=lambda ele:ele[0])
        
        labels = self.clustering(self.docs)
        self.nLabel = 0
        for i in range(len(labels)):
            self.docs[i]['label'] = labels[i]
            if labels[i] + 1 > self.nLabel:
                self.nLabel = labels[i] + 1

    ## xxx && yyy || !! ( zzz && ttt )
    def booleanQuery(self, seq, stop=0):
        stop += 1
        if(stop > 1000):
            return set()
        n = len(seq)
        if n == 0 :
            return set()
        if n == 1:
            res = set()
            if seq[0] not in self.termDict:
                return res
            idx = self.termDict[seq[0]]
            for idxItem in self.invIdxs[idx]:
                if idxItem['docId'] not in res:
                    res.add(idxItem['docId'])
            return res
        
        if seq[0] == '(' and seq[-1] == ')':
            return self.booleanQuery(seq[1:-1],stop)
        inStack = 0
        for i in range(n):
            if seq[i] == '(':
                inStack += 1
            elif seq[i] == ')':
                inStack -= 1
            elif inStack == 0:
                if seq[i] == "&&":
                    resLeft = self.booleanQuery(seq[:i],stop)
                    resRight = self.booleanQuery(seq[i+1:],stop)
                    return resLeft.intersection(resRight)
                elif seq[i] == "||":
                    resLeft = self.booleanQuery(seq[:i],stop)
                    resRight = self.booleanQuery(seq[i+1:],stop)
                    return resLeft.union(resRight)
        if seq[0] == "!!":
            res = set()
            resRight = self.booleanQuery(seq[1:],stop)
            for i in range(len(self.docs)):
                if i not in resRight:
                    res.add(i)
            return res
                    
    '''
    bound: oldest article time
    source: article source
    '''
    def specificQuery(self, bound,source=None):
        l,r,mid,ans = 0,len(self.docs)-1,-1,-1
        while l <= r:
            mid = (l + r) // 2
            if(self.invDateIdxs[mid][0] < bound):
                l = mid + 1
            else:
                ans = mid
                r = mid - 1
        ret = set()
        print("ans =",ans)
        if ans == -1:
            return ret
        else:
            for i in range(ans,len(self.invDateIdxs)):
                doc = self.invDateIdxs[i][1]
                if source == None or self.docs[doc]['source'] == source:
                    ret.add(doc)
            return ret

    '''
    query: query text
    topk: number of top results to return
    '''
    def rankedQuery(self, query,topk):
        termList = self.getTermList(query)
        res = []
        nDocs = len(self.docs)
        topk = min(topk,nDocs)
        for i in range(nDocs):
            score = 0.0
            for term in termList:
                if term not in self.termDict:
                    continue
                idx = self.termDict[term]
                termIDF = math.log2(nDocs/(self.termDF[idx]))
                termTF = 0
                for invIdx in self.invIdxs[idx]:
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
    mytool = tools()
    mytool.init()
    '''
    for key in mytool.invIdxs:
        if len(mytool.invIdxs[key]) > 2:
            print(mytool.idxDict[key],mytool.invIdxs[key])
    for i in range(10):
        print(mytool.termDF[i])
        print(mytool.invIdxs[i])
        print(mytool.idxDict[i])
    while True:
        inputLine = input()
        if inputLine == '':
            break
        now = inputLine.split(' ')
        if now[0] == 'bool':
            print('bool',now)
            print(mytool.booleanQuery(now[1:]))
        if now[0] == 'spec':
            print('spec',now)
            print(mytool.specificQuery(datetime.datetime(int(now[1]),int(now[2]),int(now[3]),int(now[4]),int(now[5])),None))
        if now[0] == 'rank':
            print('rank',now)
            print(mytool.rankedQuery(now[1],5))
            
    #init()
    #print(termDict)
    '''