from django.urls import path
from .views import (
    PostList, SearchPostList,
    NewsList, CreateNews, EditNews, DeleteNews, NewsDetail,
    ArticleList, ArticleDetail, CreateArticle, EditArticle, DeleteArticle,
    subscriptions,
)
urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('search/', SearchPostList.as_view(), name='search'),
    path('news/', NewsList.as_view(), name='news'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('news/create/', CreateNews.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', EditNews.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', DeleteNews.as_view(), name='news_delete'),
    path('articles/', ArticleList.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    path('articles/create/', CreateArticle.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', EditArticle.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', DeleteArticle.as_view(), name='article_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]
