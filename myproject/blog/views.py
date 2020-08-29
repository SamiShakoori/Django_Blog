from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from .models import Article, Category

# Create your views here.
def home(request, page=1):
    articles_list = Article.objects.filter(status='p').order_by('-publish')
    paginator = Paginator(articles_list, 2)
    # after adding page in url home then we do not need to this syntax
    # page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {
        'articles': articles,
        # 'category': Category.objects.filter(status=True)
    }
    return render(request, 'blog/home.html', context)

def detail(request, slug):
    context = {
        'article': get_object_or_404(Article, slug=slug, status='p')
    }
    return render(request, 'blog/detail.html', context)

def category(request, slug, page=1):
    category = get_object_or_404(Category, slug=slug, status=True)
    article_list = category.articles.published()
    paginator = Paginator(article_list, 2)
    articles = paginator.get_page(page)
    context = {
        'category': category,
        'articles': articles
    }
    return render(request, 'blog/category.html', context)