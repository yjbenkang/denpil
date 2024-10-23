from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField(null=True)
    nominated_year = models.IntegerField(null=True)
    description = models.TextField(null=True)

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
    rating_score = models.FloatField()
    rating_count = models.IntegerField()
    best_duration = models.CharField(max_length=200, default="default value")
    best_rank = models.IntegerField()
    publisher = models.CharField(max_length=200)
    sales_point = models.IntegerField()
    cover_url = models.URLField()
    link = models.URLField()
    age_gender_ratings = models.JSONField(default=dict, blank=True)
    stock_status = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.title


class BookSalesInfo(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name="sales_info")

    # 가격 관련 필드
    pricesales = models.IntegerField()  # 실제 판매 가격
    pricestandard = models.IntegerField()  # 정가
    discount_price = models.IntegerField()  # 할인가
    discount_rate = models.FloatField()  # 할인율 (백분율로 저장)

    # 판매 지수
    sales_point = models.IntegerField()  # 판매 지수

    def __str__(self):
        return f"{self.book.title} - 판매 정보"

class PublisherSalesData(models.Model):
    publisher = models.CharField(max_length=200)  # 출판사 이름
    total_sales = models.IntegerField()  # 총 판매량 (sales_point 합계)
    book_count = models.IntegerField()  # 출판사별 책 개수

    def __str__(self):
        return f"{self.publisher} - 총 판매량: {self.total_sales}, 책 개수: {self.book_count}"

class BookAgeGenderData(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="age_gender_data")

    # 연령대별 데이터
    age_10 = models.FloatField(default=0.0)
    age_20 = models.FloatField(default=0.0)
    age_30 = models.FloatField(default=0.0)
    age_40 = models.FloatField(default=0.0)
    age_50 = models.FloatField(default=0.0)
    age_60 = models.FloatField(default=0.0)

    # 성별 데이터
    male = models.FloatField(default=0.0)
    female = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.book.title} - 연령/성별 데이터"

class AuthorAgeGenderData(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author_age_gender_data")

    # 연령대별 데이터
    age_10 = models.FloatField(default=0.0)
    age_20 = models.FloatField(default=0.0)
    age_30 = models.FloatField(default=0.0)
    age_40 = models.FloatField(default=0.0)
    age_50 = models.FloatField(default=0.0)
    age_60 = models.FloatField(default=0.0)

    # 성별 데이터
    male = models.FloatField(default=0.0)
    female = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.author.name} - 연령/성별 데이터"