from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    pubdate = models.DateField()
    description = models.TextField()
    pricesales = models.IntegerField() # 회의로 넣을지 결정
    pricestandard = models.IntegerField() #회의로 넣을지 결정
    publisher = models.CharField(max_length=200)
    sales_point = models.IntegerField()
    cover_url = models.URLField()
    link = models.URLField()

    def __str__(self):
        return self.title


