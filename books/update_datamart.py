from asgiref.sync import sync_to_async
from .models import Book, BookSalesInfo, PublisherSalesData, BookAgeGenderData, AuthorAgeGenderData
import pandas as pd


@sync_to_async
def update_book_sales_info():
    # Book 모델에서 필요한 필드를 가져옵니다
    books = Book.objects.all().values('id', 'pricesales', 'pricestandard', 'sales_point')

    # 쿼리셋을 pandas DataFrame으로 변환
    df = pd.DataFrame(list(books))

    # 할인가 계산 (정가 - 판매가)
    df['discount_price'] = df['pricestandard'] - df['pricesales']

    # 할인율 계산 ((1 - 판매가 / 정가) * 100)
    df['discount_rate'] = ((1 - df['pricesales'] / df['pricestandard']) * 100).round(2)

    # BookSalesInfo 데이터 저장 전에 기존 데이터 삭제
    BookSalesInfo.objects.all().delete()

    # pandas DataFrame에서 각 책에 대한 판매 정보 저장
    for _, row in df.iterrows():
        book = Book.objects.get(id=row['id'])
        BookSalesInfo.objects.create(
            book=book,
            pricesales=row['pricesales'],
            pricestandard=row['pricestandard'],
            discount_price=row['discount_price'],
            discount_rate=row['discount_rate'],
            sales_point=row['sales_point']
        )

    print("BookSalesInfo 데이터 업데이트 완료")

@sync_to_async
def update_publisher_sales_point():
    # Book 모델에서 데이터를 가져옵니다
    books = Book.objects.all().values('publisher', 'sales_point')

    # 쿼리셋을 pandas DataFrame으로 변환
    df = pd.DataFrame(list(books))

    # 출판사별로 책 개수와 판매량을 계산
    grouped_data = df.groupby('publisher').agg(
        total_sales=('sales_point', 'sum'),  # 총 판매량
        book_count=('publisher', 'count')  # 책의 개수
    ).reset_index()

    # 기존 데이터 삭제 (필요시)
    PublisherSalesData.objects.all().delete()

    # 결과를 PublisherSalesData 모델에 저장
    for _, row in grouped_data.iterrows():
        PublisherSalesData.objects.create(
            publisher=row['publisher'],
            total_sales=row['total_sales'],
            book_count=row['book_count']
        )

    print("출판사별 판매량/총 출판 책 개수 데이터 업데이트 완료")

@sync_to_async
def update_book_age_gender_data():
    # Book 모델에서 데이터를 가져옵니다
    books = Book.objects.all().values('id', 'age_gender_ratings')

    # 쿼리셋을 DataFrame으로 변환
    df = pd.DataFrame(list(books))

    # age_gender_ratings JSON 데이터를 펼칩니다 (normalize)
    ratings_df = pd.json_normalize(df['age_gender_ratings'])

    # 나이대별 데이터를 합산
    df['age_10'] = ratings_df['10대 여성'].fillna(0) + ratings_df['10대 남성'].fillna(0)
    df['age_20'] = ratings_df['20대 여성'].fillna(0) + ratings_df['20대 남성'].fillna(0)
    df['age_30'] = ratings_df['30대 여성'].fillna(0) + ratings_df['30대 남성'].fillna(0)
    df['age_40'] = ratings_df['40대 여성'].fillna(0) + ratings_df['40대 남성'].fillna(0)
    df['age_50'] = ratings_df['50대 여성'].fillna(0) + ratings_df['50대 남성'].fillna(0)
    df['age_60'] = ratings_df['60대 이상 여성'].fillna(0) + ratings_df['60대 이상 남성'].fillna(0)

    # 성별 데이터를 합산
    df['male'] = (
        ratings_df['10대 남성'].fillna(0) + ratings_df['20대 남성'].fillna(0) +
        ratings_df['30대 남성'].fillna(0) + ratings_df['40대 남성'].fillna(0) +
        ratings_df['50대 남성'].fillna(0) + ratings_df['60대 이상 남성'].fillna(0)
    )
    df['female'] = (
        ratings_df['10대 여성'].fillna(0) + ratings_df['20대 여성'].fillna(0) +
        ratings_df['30대 여성'].fillna(0) + ratings_df['40대 여성'].fillna(0) +
        ratings_df['50대 여성'].fillna(0) + ratings_df['60대 이상 여성'].fillna(0)
    )

    # 데이터 저장 전에 기존 데이터를 모두 삭제합니다
    BookAgeGenderData.objects.all().delete()

    # pandas에서 각 데이터를 데이터베이스에 저장
    for _, row in df.iterrows():
        BookAgeGenderData.objects.create(
            book_id=row['id'],
            age_10=row['age_10'],
            age_20=row['age_20'],
            age_30=row['age_30'],
            age_40=row['age_40'],
            age_50=row['age_50'],
            age_60=row['age_60'],
            male=row['male'],
            female=row['female']
        )

    print("책 연령/성별 데이터 업데이트 완료")


@sync_to_async
def update_author_age_gender_data():
    # 모든 책 데이터를 가져옵니다 (책 정보에 연령/성별 정보 포함)
    books = Book.objects.all().values('author_id', 'age_gender_ratings')

    # 쿼리셋을 pandas DataFrame으로 변환
    df = pd.DataFrame(list(books))

    # JSON 데이터인 age_gender_ratings를 펼쳐서 각각의 열로 분리
    ratings_df = pd.json_normalize(df['age_gender_ratings'])

    # 나이대별 데이터를 합산 (작가별로)
    df['age_10'] = ratings_df['10대 여성'].fillna(0) + ratings_df['10대 남성'].fillna(0)
    df['age_20'] = ratings_df['20대 여성'].fillna(0) + ratings_df['20대 남성'].fillna(0)
    df['age_30'] = ratings_df['30대 여성'].fillna(0) + ratings_df['30대 남성'].fillna(0)
    df['age_40'] = ratings_df['40대 여성'].fillna(0) + ratings_df['40대 남성'].fillna(0)
    df['age_50'] = ratings_df['50대 여성'].fillna(0) + ratings_df['50대 남성'].fillna(0)
    df['age_60'] = ratings_df['60대 이상 여성'].fillna(0) + ratings_df['60대 이상 남성'].fillna(0)

    # 성별 데이터를 합산 (작가별로)
    df['male'] = (
        ratings_df['10대 남성'].fillna(0) + ratings_df['20대 남성'].fillna(0) +
        ratings_df['30대 남성'].fillna(0) + ratings_df['40대 남성'].fillna(0) +
        ratings_df['50대 남성'].fillna(0) + ratings_df['60대 이상 남성'].fillna(0)
    )
    df['female'] = (
        ratings_df['10대 여성'].fillna(0) + ratings_df['20대 여성'].fillna(0) +
        ratings_df['30대 여성'].fillna(0) + ratings_df['40대 여성'].fillna(0) +
        ratings_df['50대 여성'].fillna(0) + ratings_df['60대 이상 여성'].fillna(0)
    )

    # 작가별로 데이터를 그룹화하여 합산
    grouped_data = df.groupby('author_id').agg(
        total_age_10=('age_10', 'sum'),
        total_age_20=('age_20', 'sum'),
        total_age_30=('age_30', 'sum'),
        total_age_40=('age_40', 'sum'),
        total_age_50=('age_50', 'sum'),
        total_age_60=('age_60', 'sum'),
        total_male=('male', 'sum'),
        total_female=('female', 'sum')
    ).reset_index()

    # 각 작가의 총 연령대 및 성별 비율 계산
    grouped_data['total_age'] = (
            grouped_data['total_age_10'] + grouped_data['total_age_20'] +
            grouped_data['total_age_30'] + grouped_data['total_age_40'] +
            grouped_data['total_age_50'] + grouped_data['total_age_60']
    )

    grouped_data['total_gender'] = grouped_data['total_male'] + grouped_data['total_female']

    # 각 연령대와 성별의 비율 계산
    grouped_data['age_10_ratio'] = grouped_data['total_age_10'] / grouped_data['total_age'] * 100
    grouped_data['age_20_ratio'] = grouped_data['total_age_20'] / grouped_data['total_age'] * 100
    grouped_data['age_30_ratio'] = grouped_data['total_age_30'] / grouped_data['total_age'] * 100
    grouped_data['age_40_ratio'] = grouped_data['total_age_40'] / grouped_data['total_age'] * 100
    grouped_data['age_50_ratio'] = grouped_data['total_age_50'] / grouped_data['total_age'] * 100
    grouped_data['age_60_ratio'] = grouped_data['total_age_60'] / grouped_data['total_age'] * 100

    grouped_data['male_ratio'] = grouped_data['total_male'] / grouped_data['total_gender'] * 100
    grouped_data['female_ratio'] = grouped_data['total_female'] / grouped_data['total_gender'] * 100

    # 데이터 저장 전에 기존 데이터를 모두 삭제합니다
    AuthorAgeGenderData.objects.all().delete()

    # pandas DataFrame에서 각 작가에 대한 데이터 저장
    for _, row in grouped_data.iterrows():
        AuthorAgeGenderData.objects.create(
            author_id=row['author_id'],
            age_10=row['age_10_ratio'],
            age_20=row['age_20_ratio'],
            age_30=row['age_30_ratio'],
            age_40=row['age_40_ratio'],
            age_50=row['age_50_ratio'],
            age_60=row['age_60_ratio'],
            male=row['male_ratio'],
            female=row['female_ratio']
        )

    print("작가별 연령/성별 데이터 업데이트 완료")