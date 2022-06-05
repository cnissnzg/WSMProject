from django.db.models import Q
from django.shortcuts import render
import dateutil.parser
from .models import Post
import searching.engine.dataloader
from searching.engine.algorithm import tools

tool = tools()
tool.init()

def index(request):
    return render(request,'base.html')

def search(request):
    key = request.GET.get('key')
    cate = request.GET.get('group')
    error_msg = ''
    if not key:
        error_msg = "请输入关键词"
        return render(request, 'index.html', {'error_msg': error_msg})

    if cate == '1':
        bq = tool.rankedQuery(key, 15)
    elif cate == '3':
        print(tool.termDict)
        bq = tool.booleanQuery(key.split())

    else:
        bq = tool.specificQuery(dateutil.parser.parse(key))

    print(bq)
    post_list = []
    for i in bq:
        post_list.append(tool.docs[i])

    # post_list = Post.objects.filter(Q(title__icontains=key) | Q(content__icontains=key))
    return render(request, 'index.html', {'error_msg': error_msg, 'post_list': post_list})
