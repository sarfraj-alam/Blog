# Generated by Django 3.0.6 on 2020-06-21 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogcomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogcomment',
            old_name='comments',
            new_name='comment',
        ),
    ]
