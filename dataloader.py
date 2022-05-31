from cgitb import text
import json
from posixpath import split
import os

def getDocs(path='data'):
    objs = []
    listDir=os.listdir(path)
    for fileName in listDir:
        with open('data/'+fileName,'r') as f:
            texts = f.read().split('\n')
            for text in texts:
                if len(text) == 0:
                    continue
                objs.append(json.loads(text))
    print('loads {} documents from files {}'.format(len(objs),str(listDir)))
    return objs

getDocs()