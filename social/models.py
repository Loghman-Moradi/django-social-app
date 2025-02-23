from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateField(verbose_name="تاریخ تولد", blank=True, null=True)
    bio = models.TextField(verbose_name="بایو", blank=True, null=True)
    job = models.CharField(verbose_name="شغل", max_length=50, blank=True, null=True)
    photo = models.ImageField(verbose_name="تصویر", blank=True, null=True)
    phone = models.CharField(verbose_name="تلفن", blank=True, null=True, max_length=11)
    following = models.ManyToManyField('self', through='Contact', related_name="followers", symmetrical=False)

    def get_followers(self):
        return [contact.user_from for contact in self.rel_to_set.all().order_by('-created')]

    def get_following(self):
        return [contact.user_to for contact in self.rel_to_set.all().order_by('-created')]


class Post(models.Model):
    author = models.ForeignKey(User, models.CASCADE, related_name="user_posts", verbose_name="نویسنده")
    description = models.TextField(verbose_name="توضیحات")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    total_likes = models.PositiveIntegerField(default=0)
    saves = models.ManyToManyField(User, related_name="saved_posts")
    active = models.BooleanField(default=True)
    tags = TaggableManager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-total_likes']),
        ]

        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    def __str__(self):
        return self.author.first_name

    def get_absolute_url(self):
        return reverse('social:post_detail', args=[self.id])


class Ticket(models.Model):
    user_ticket_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_ticket")
    fullname = models.CharField(max_length=120, verbose_name="نام و نام خانوادگی")
    email = models.EmailField(max_length=50, verbose_name="ایمیل")
    phone_number = models.CharField(max_length=11, verbose_name="شماره تلفن")
    message = models.TextField(max_length=500, verbose_name="متن")
    subject = models.CharField(max_length=50, verbose_name="موضوع")
    created = models.DateTimeField(auto_now_add=True)
    admin_response = models.TextField(max_length=500, verbose_name="پاسخ ادمین", blank=True, null=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"

    def __str__(self):
        return self.subject


class Comment(models.Model):
    post = models.ForeignKey(Post, models.CASCADE, related_name="comments", verbose_name="پست")
    name = models.CharField(max_length=50, verbose_name="نام")
    description = models.TextField(max_length=250, verbose_name="متن")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return f"{self.name}: {self.post}"


class Image(models.Model):
    post = models.ForeignKey(Post, models.CASCADE, related_name="images")
    file_image = models.ImageField(upload_to="images")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

        verbose_name = "تصویر"
        verbose_name_plural = "تصویرها"

    def __str__(self):
        return self.file_image.name


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name="rel_from_set", on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name="rel_to_set", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


























