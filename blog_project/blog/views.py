from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator


@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user)

    return render(request, 'blog/profile.html', {
        'posts': posts
    })


@login_required
def home(request):
    query = request.GET.get('q')
    post_list = Post.objects.all().order_by('-created')

    if query:
        post_list = post_list.filter(title__icontains=query)

    paginator = Paginator(post_list, 4)  # 4 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')

    return render(request, 'blog/home.html', {
        'posts': posts,
        'form': form
    })

def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'registration/register.html', {'form': form})


# def home(request):
#     query = request.GET.get('q')
#     posts = Post.objects.all()
#
#     if query:
#         posts = posts.filter(title__icontains=query)
#
#     form = PostForm()
#
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             form.save()
#             return redirect('home')
#
#     return render(request, 'blog/home.html', {'posts': posts, 'form': form})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        return redirect('home')

    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'blog/edit_post.html', {'form': form})


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return render(request, 'blog/delete_post.html', {'post': post})
