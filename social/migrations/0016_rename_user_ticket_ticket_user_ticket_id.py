# Generated by Django 5.1.2 on 2024-11-01 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0015_ticket_user_ticket'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='user_ticket',
            new_name='user_ticket_id',
        ),
    ]
