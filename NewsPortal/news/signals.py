from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post


@receiver(m2m_changed, sender=Post.categories.through)
def post_created(sender, instance, action, model, pk_set, **kwargs):
    if action == 'post_add':
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
            f'{instance.title}'
            f'{instance.preview()}'
            f'Читать далее: {instance.get_absolute_url()}'
        )
        html_content = (
            f'<h1>{instance.title}</h1><br>'
            f'<p>{instance.preview()}</p>'
            f'<a href="{instance.get_absolute_url()}">Читать далее</a>'
        )
        for email, categories in subscribers_emails.items():
            title = 'Новая статья ' if instance.position == "AR" else 'Новая новость '
            title += 'в избранной категории - ' if len(categories) == 1 else 'в избранных категориях - '
            categories = ', '.join(categories)
            title += categories
            print(title, '\n', text_content)
            msg = EmailMultiAlternatives(title, text_content, 'egor-shiryaev2013@yandex.ru', [email])
            msg.attach_alternative(html_content, 'text/html')

