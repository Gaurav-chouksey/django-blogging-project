from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import render, get_object_or_404, redirect
from .forms import SignUpForm, CommentForm, PostForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q  # Import Q for complex queries
from django.http import HttpResponseForbidden


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer


def post_list(request):
    # Get the query parameter
    query = request.GET.get('q')
    # Convert "None" string or None value to an empty string
    if not query or query.lower() == 'none':
        query = ''
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__icontains=query)
        ).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after a successful signup
        else:
            print(form.errors)  # Temporarily print errors for debugging
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # include request.FILES
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user   # Set the current user as the comment author
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created_at')
    comments = Comment.objects.filter(author=user).order_by('-created_at')
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Optionally, you can add a success message here
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)
    
    context = {
        'posts': posts,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Only allow the post author to update the post
    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to edit this post.")
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Only allow the post author to delete the post
    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        return HttpResponseForbidden("You are not allowed to edit this comment.")
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
    
    if request.method == 'POST':
        post_pk = comment.post.pk
        comment.delete()
        return redirect('post_detail', pk=post_pk)
    
    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    referrer = request.META.get('HTTP_REFERER')
    if referrer:
        return redirect(referrer)
    else:
        return redirect('post_detail', pk=post.pk)



@login_required
def comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user
    if user in comment.likes.all():
        comment.likes.remove(user)
    else:
        comment.likes.add(user)
    referrer = request.META.get('HTTP_REFERER')
    if referrer:
        return redirect(referrer)
    else:
        return redirect('post_detail', pk=comment.post.pk)
