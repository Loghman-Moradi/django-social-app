from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.core.mail import send_mail



@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'phone', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('ADAdditional information', {'fields': ('date_of_birth', 'bio', 'photo', 'job', 'phone')}),
    )


@admin.action(description='رد پست')
def make_deactivate(modeladmin, request, queryset):
    queryset.update(active=False)

    for post in queryset:
        author_email = post.author.email
        subject = "پست شما رد شد."
        message = (f"سلام پست شما به دلایل نامشخص رد شده است...\n"
                   f"ایدی:{post.id}\n"
                   f"اسم پست:{post.description}\n")
        if author_email:
            try:
                send_mail(subject, message, "developer.9950@gmail.com", [post.author.email],
                          fail_silently=False)
            except Exception as e:
                modeladmin.message_user(request, f"There is a problem sending the email!!!", str(e))


@admin.action(description="تایید پست")
def make_activate(modeladmin, request, queryset):
    queryset.update(active=True)

    for post in queryset:
        author_email = post.author.email
        subject = "تایید پست."
        message = (f"سلام پست شما تایید شده است...\n"
                   f"ایدی:{post.id}\n"
                   f"اسم پست:{post.description}\n")
        if author_email:
            try:
                send_mail(subject, message, "developer.9950@gmail.com", [post.author.email],
                          fail_silently=False)
            except Exception as e:
                modeladmin.message_user(request, f"There is a problem sending the email!!!", str(e))


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'created', 'description']
    ordering = ['created']
    search_fields = ['description']
    actions = [make_deactivate, make_activate]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'phone_number', 'subject', 'created']
    fields = ['fullname', 'email', 'phone_number', 'subject', 'message', 'admin_response']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'created']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to']
