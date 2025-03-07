# Generated by Django 5.1.2 on 2024-10-28 17:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0009_alter_post_saves_contact'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='social.Contact', to=settings.AUTH_USER_MODEL),
        ),
    ]
