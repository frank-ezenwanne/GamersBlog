# Generated by Django 3.0.7 on 2020-07-20 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='body',
            new_name='comment_body',
        ),
    ]
