from django.db import models

# Create your models here.


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=200, unique=True)
    title_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.author + ' ' + str(self.title_count)


class Title(models.Model):
    author_id = models.IntegerField()
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

