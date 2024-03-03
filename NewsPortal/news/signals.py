from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post
from .tasks import post_add_task


@receiver(m2m_changed, sender=Post.categories.through)
def post_created(sender, instance, action, model, pk_set, **kwargs):
    if action == 'post_add':
        post_add_task.delay(instance.id)

