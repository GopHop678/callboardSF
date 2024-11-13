from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Response


@receiver(post_save, sender=Response)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        author_email = post.author.email

        if author_email:
            subject = f'Вам готовы помочь!'
            message = \
                f'Пользователь {instance.user.username} оставил свой отклик на Ваше объявление "{post}"\n\n' \
                f'Содержание:\n' \
                f'{instance.response_text}'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [author_email])
