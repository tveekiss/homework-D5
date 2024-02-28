import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.utils import timezone
from datetime import timedelta

from django.core.mail import EmailMultiAlternatives

from news.models import Post, Subscriber

logger = logging.getLogger(__name__)


def my_job():
    for subscription in Subscriber.objects.select_related('category', 'user'):
        category_name = subscription.category.category
        user = subscription.user.username
        user_email = subscription.user.email

        last_notification_date = timezone.now() - timedelta(days=7)

        new_posts = set(Post.objects.filter(date__gt=last_notification_date, categories__category=category_name))

        subject = 'Новые посты за неделю'
        text_content = ''
        for post in new_posts:
            text_content += post.title + '\n'
            text_content += post.preview() + '\n'
            text_content += f'Читать далее: {post.get_absolute_url()}\n\n'
        html_content = ''
        for post in new_posts:
            html_content += f'<h1>{post.title}</h1><br>'
            html_content += f'<p>{post.preview()} <a href="{post.get_absolute_url()}">.Читать далее</a></p><br>'
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        # print(f'subject: {subject}')
        # print(f'from: {settings.DEFAULT_FROM_EMAIL}')
        # print(f'to: {user_email}')
        # print(f'content:\n {text_content}')
        # print('')





# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")