from django.db.models import Q
from django.shortcuts import render
from .models import Post

def index(request):
    return render(request,'base.html')

def search(request):
    key = request.GET.get('key')
    cate = request.GET.get('group')
    error_msg = ''
    if not key:
        error_msg = "请输入关键词"
        return render(request, 'index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=key) | Q(content__icontains=key))
    return render(request, 'index.html', {'error_msg': error_msg, 'post_list': post_list})
