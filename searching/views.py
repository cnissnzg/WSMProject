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
    group = request.GET.get('group')
    cate = request.GET.get('category')
    error_msg = ''
    if not key:
        error_msg = "请输入关键词"
        return render(request, 'index.html', {'error_msg': error_msg})

    if group == '1':
        bq = tool.rankedQuery(key, 15)
    elif group == '3':
        print(tool.termDict)
        bq = tool.booleanQuery(key.split())
    else:
        bq = tool.specificQuery(dateutil.parser.parse(key))

    print(bq)
    post_list = []
    for i in bq:
        if cate=='0':
            post_list.append(tool.docs[i])
        else:
            if (tool.docs[i]['label'] + 1) == int(cate):
                post_list.append(tool.docs[i])

    # post_list = Post.objects.filter(Q(title__icontains=key) | Q(content__icontains=key))
    return render(request, 'index.html', {'error_msg': error_msg, 'post_list': post_list})
