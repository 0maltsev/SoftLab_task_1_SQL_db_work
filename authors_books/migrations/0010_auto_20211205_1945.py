# Generated by Django 3.2.9 on 2021-12-05 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors_books', '0009_remove_author_title_count'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Title',
        ),
    ]