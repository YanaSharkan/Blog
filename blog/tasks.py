from core.celery import app

from django.core.mail import send_mail


@app.task
def send_feedback(email, text):
    send_mail(
        'Feedback from user',
        text,
        'user@blog.com',
        [email],
        fail_silently=False,
    )


@app.task
def send_content_notification(email, title, text):
    send_mail(
        title,
        text,
        'user@blog.com',
        [email],
        fail_silently=False,
    )
