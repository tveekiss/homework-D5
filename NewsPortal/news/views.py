from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django_filters.views import FilterView
from .models import Post
from .filters import PostFilters
from .forms import Newsform, ArticleForm


# ===============POSTS===============
class PostList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class SearchPostList(FilterView):
    model = Post
    filterset_class = PostFilters
    template_name = 'posts/posts_search.html'


# ===============NEWS===============
class NewsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts/news/news_list.html'
    context_object_name = 'news'
    paginate_by = 10
    queryset = Post.objects.filter(position='NW')


class NewsDetail(DetailView):
    model = Post
    template_name = 'posts/news/news_detail.html'
    context_object_name = 'new'


class CreateNews(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = Newsform
    model = Post
    template_name = 'posts/news/news_create.html'
    success_url = reverse_lazy('news')

    def form_valid(self, form):
        news = form.save(commit=False)
        news.position = 'NW'
        return super().form_valid(form)


class EditNews(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = Newsform
    model = Post
    template_name = 'posts/news/news_create.html'
    success_url = reverse_lazy('news')


class DeleteNews(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'posts/news/news_delete.html'
    success_url = reverse_lazy('news')


# ===============ARTICLES===============

class ArticleList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts/articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    queryset = Post.objects.filter(position='AR')


class ArticleDetail(DetailView):
    model = Post
    template_name = 'posts/articles/article_detail.html'
    context_object_name = 'article'


class CreateArticle(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = ArticleForm
    model = Post
    template_name = 'posts/articles/article_create.html'
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        news = form.save(commit=False)
        news.position = 'AR'
        return super().form_valid(form)


class EditArticle(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = Newsform
    model = Post
    template_name = 'posts/articles/article_create.html'
    success_url = reverse_lazy('articles')


class DeleteArticle(DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'posts/articles/article_delete.html'
    success_url = reverse_lazy('articles')
