from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver
from .models import Post, User
from django.core.mail import send_mail


@receiver(m2m_changed, sender=Post.likes.through)
def user_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()


@receiver(post_delete, sender=Post)
def post_delete_handler(sender, instance, **kwargs):
    author = instance.author
    subject = f"Your post has been deleted..."
    message = f"Your post has been deleted (ID: {instance.id})"
    send_mail(subject, message, "developer.9950@gmail.com", [author.email],
              fail_silently=False)


@receiver(post_save, sender=User)
def default_info_save(sender, instance, created, **kwargs):
    if created:
        instance.bio = "No bio"
        instance.job = "......"
        instance.date_of_birth = None
        instance.save()






































