from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from .models import Post, Group, User
from .forms import PostForm
from .utils import post_paginator


def index(request):
    context = {'page_obj': post_paginator(Post.objects.all(), request)}
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    context = {
        'group': group,
        'page_obj': post_paginator(group.posts.all(), request),
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    quantity = author.posts.select_related('author').count()
    context = {
        'author': author,
        'quantity': quantity,
        'page_obj': post_paginator(
            author.posts.select_related('author'),
            request
        ),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    quantity = Post.objects.select_related(
        'author').filter(author=post.author).count()
    context = {
        'post': post,
        'quantity': quantity,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('posts:profile', post.author)
    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id)
        context = {
            'is_edit': is_edit,
            'post': post,
            'form': form,
        }
        return render(request, 'posts/post_create.html', context)
    return render(request, 'posts/post_create.html', context)
