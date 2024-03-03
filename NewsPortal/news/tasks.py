from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context
from datetime import datetime, timedelta


from .models import Post, Subscriber


@shared_task
def post_add_task(post_id):
    print(f'post_id: {post_id}')
    instance = Post.objects.get(pk=post_id)
    categories = instance.categories.all()
    subscribers_emails = {}
    for category in categories:
        subscribers = category.subscribers.all()
        for subscriber in subscribers:
            if subscriber.user.email in subscribers_emails.keys():
                subscribers_emails[subscriber.user.email].append(category.category)
            else:
                subscribers_emails[subscriber.user.email] = []
                subscribers_emails[subscriber.user.email].append(category.category)
    text_content = (
        f'{instance.title}\n'
        f'{instance.preview()}'
        f'Читать далее: {instance.get_absolute_url()}'
    )
    html_content = (
        f'<h1>{instance.title}</h1><br>'
        f'<p>{instance.preview()}'
        f'<a href="{instance.get_absolute_url()}">Читать далее</a></p>'
    )
    for email, categories in subscribers_emails.items():
        title = 'Новая статья ' if instance.position == "AR" else 'Новая новость '
        title += 'в избранной категории - ' if len(categories) == 1 else 'в избранных категориях - '
        categories = ', '.join(categories)
        title += categories
        print(title, '\n', text_content)
        msg = EmailMultiAlternatives(title, text_content, 'egor-shiryaev2013@yandex.ru', [email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def mailing():
    for subscription in Subscriber.objects.select_related('category', 'user'):
        category_name = subscription.category.category
        user = subscription.user.username
        user_email = subscription.user.email

        last_notification_date = datetime.now() - timedelta(days=7)

        new_posts = set(Post.objects.filter(date__gt=last_notification_date, categories__category=category_name))

        subject = 'Новые посты за неделю'
        text_content = ''

        html_template = Template('''
        <h1>{{ post.title }}</h1><br>
        <p>{{ post.preview }}</p> <a href="{{ post.get_absolute_url }}">Читать далее</a></p><br>
        ''')

        for post in new_posts:
            text_content += post.title + '\n'
            text_content += post.preview() + '\n'
            text_content += f'Читать далее: {post.get_absolute_url()}\n\n'
        html_content = ''
        for post in new_posts:
            html_content += html_template.render(Context({'post': post}))
        msg = EmailMultiAlternatives(subject, text_content, 'egor-shiryaev2013@yandex.ru', [user_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
