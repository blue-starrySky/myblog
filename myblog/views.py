from django.shortcuts import render
from django import forms
from django.shortcuts import render,render_to_response

from .models import *
from django.http import Http404
# Create your views here.
"""
借此完成博客的评论功能
"""

class CommentForm(forms.Form):

    name=forms.CharField(label='称呼',max_length=16,error_messages={
        'required':'请填写您的称呼',
        'max_length':'称呼太长咯'
    })
    email=forms.EmailField(label='邮箱',error_messages={
        'required':'请填写您的邮箱',
        'invalid':'邮箱格式不正确'
    })
    content=forms.CharField(label='内容',error_messages={
        'required':'请填写您的评论内容!',
        'max_length':'评论内容太长咯'
    })
def get_blogs(request):
    blogs=Blog.objects.all().order_by('-pub')#获得所有的博客按时间排序
    return render_to_response('blog_list.html',{'blogs':blogs})#传递context:blog参数到固定页面。

def get_details(request,blog_id):
#检查异常
    try:
        blog=Blog.objects.get(id=blog_id)#获取固定的blog_id的对象；
    except Blog.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        form = CommentForm()
    else:#请求方法为Post
        form = CommentForm(request.POST)
        if form.is_valid():
            cleaned_data=form.cleaned_data
            cleaned_data['blog']=blog
            Comment.objects.create(**cleaned_data)
    ctx={
        'blog':blog,
        'comments': blog.comment_set.all().order_by('-pub'),
        'form': form
    }#返回3个参数
    return render(request,'blog_details.html',ctx)