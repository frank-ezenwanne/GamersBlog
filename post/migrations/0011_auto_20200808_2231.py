# Generated by Django 3.0.7 on 2020-08-08 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_auto_20200808_2205'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='replied_commentid',
            new_name='repliedcomid',
        ),
    ]
