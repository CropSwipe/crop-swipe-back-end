# Generated by Django 3.2 on 2023-06-25 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crop', '0007_alter_like_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='author',
            new_name='user',
        ),
    ]
