from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_rating = self.post_set.aggregate(post_rating=Sum('rating'))
        result_sum_rating = 0
        try:
            result_sum_rating += sum_rating.get('rating')
        except TypeError:
            result_sum_rating = 0

        sum_comment_rating = self.user.comment_set.aggregate(comment_rating=Sum('comment_rating'))
        result_sum_comment_rating = 0
        result_sum_comment_rating += sum_comment_rating.get('comment_rating')

        # суммарный рейтинг каждой статьи автора умноженный на 3
        self.user_rating = result_sum_rating * 3 + result_sum_comment_rating
        # сохраняем результаты в базу данных
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category.title()


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    article = 'AR'
    news = 'NW'

    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    position = models.CharField(max_length=2,
                                choices=POSITIONS,
                                default=article)
    date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return (self.text[:124] + '...') if self.text else 'Текст не найден'

    def __str__(self):
        return f'{self.title}: {self.text}'

    def get_absolute_url(self):
        post = 'news' if self.position == 'NW' else 'articles'
        return 'http://127.0.0.1:8000/' + post + '/' + str(self.pk) + '/'



class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    past = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_of_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class Subscriber(models.Model):
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='subscribers')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscribers')
