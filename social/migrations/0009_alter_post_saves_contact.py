# Generated by Django 5.1.2 on 2024-10-28 10:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0008_post_saves'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='saves',
            field=models.ManyToManyField(related_name='saved_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_from_set', to=settings.AUTH_USER_MODEL)),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_to_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
                'indexes': [models.Index(fields=['-created'], name='social_cont_created_5581d1_idx')],
            },
        ),
    ]
