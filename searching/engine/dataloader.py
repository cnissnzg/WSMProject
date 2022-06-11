# encoding=utf-8
from cgitb import text
import json
from posixpath import split
import os
import random
from dateutil.parser import parse
import datetime


def getDocs(path='data'):
    objs = []
    listDir=os.listdir(path)
    for fileName in listDir:
        with open('data/'+fileName,'r',encoding='utf-8') as f:
            texts = f.read().split('\n')
            for text in texts:
                if len(text) == 0:
                    continue
                obj = json.loads(text)
                try:
                    obj['parseTime'] = parse(obj['time'])
                except:
                    obj['parseTime'] = datetime.datetime.now()
                objs.append(obj)
    print('loads {} documents from files {}'.format(len(objs),str(listDir)))
    random.shuffle(objs)
    return objs[:300]

if __name__ == "__main__":
    getDocs()