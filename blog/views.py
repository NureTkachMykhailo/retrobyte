from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from rest_framework import viewsets

from .forms import ArticleForm, CommentForm, RegisterForm
from .models import Article, Category, Comment
from .serializers import ArticleSerializer


def category_list(request):
    categories = Category.objects.annotate(article_count=Count('articles'))
    return render(request, 'blog/category_list.html', {'categories': categories})


def article_list(request):
    articles = Article.objects.select_related('category', 'author').annotate(
        comment_count=Count('comments')
    )

    category_id = request.GET.get('category')
    if category_id:
        articles = articles.filter(category_id=category_id)

    query = request.GET.get('q')
    if query:
        articles = articles.filter(title__icontains=query) | articles.filter(text__icontains=query)

    sort_by = request.GET.get('sort', '-published_date')
    if sort_by in ['published_date', '-published_date', 'comment_count', '-comment_count']:
        articles = articles.order_by(sort_by)

    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/article_list.html',
        {
            'page_obj': page_obj,
            'categories': Category.objects.all(),
            'query': query or '',
            'sort_by': sort_by,
            'selected_category': category_id or '',
        },
    )


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.select_related('author').order_by('-comment_date')

    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    comment_page = paginator.get_page(page_number)

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article_detail', pk=pk)
    else:
        form = CommentForm()

    return render(
        request,
        'blog/article_detail.html',
        {'article': article, 'comment_page': comment_page, 'form': form},
    )


@login_required
def my_articles(request):
    articles = Article.objects.filter(author=request.user).order_by('-published_date')
    return render(request, 'blog/my_articles.html', {'articles': articles})


@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form, 'title': 'Нова стаття'})


@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author != request.user and not request.user.is_staff:
        return redirect('article_detail', pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_form.html', {'form': form, 'title': 'Редагування статті'})


@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author == request.user or request.user.is_staff:
        article.delete()
    return redirect('article_list')


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    article_pk = comment.article_id
    if comment.author == request.user or request.user.is_staff:
        comment.delete()
    return redirect('article_detail', pk=article_pk)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('category_list'))
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.select_related('category', 'author').all()
    serializer_class = ArticleSerializer
