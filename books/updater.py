import requests
import json
from apscheduler.schedulers.background import BackgroundScheduler
from pathlib import Path
from .models import Book, Author

scheduler = BackgroundScheduler()
BASE_DIR = Path(__file__).resolve().parent.parent


def get_secret(key):
    with open(BASE_DIR / 'secrets.json') as f:
        secrets = json.load(f)
    try:
        return secrets[key]
    except KeyError:
        raise EnvironmentError(f"Set the {key} environment variable.")


def update_data(author):
    key = get_secret('TTB_KEY')
    search_url = f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={key}&Query={author}&QueryType=Author&MaxResults=100&start=1&SearchTarget=Book&output=js&Version=20131101"
    response = requests.get(search_url)
    data = json.loads(response.text)

    # 데이터 전처리
    items = data.get('item', [])
    print(len(items))
    for item in items:
        title = item.get('title', '')
        pub_date = item.get('pubDate', '')
        description = item.get('description', '')
        salesPoint = item.get('salesPoint', 0)
        cover = item.get('cover', '')
        publisher = item.get('publisher', '')
        price_sales = item.get('priceSales', 0)
        price_standard = item.get('priceStandard', 0)
        bestDuration = item.get('bestDuration', '')
        bestRank = item.get('bestRank', 0)
        link = item.get('link', '')
        isbn13 = item.get('isbn13', '')
        
        if isbn13:  # isbn13이 존재할 때만 추가 정보를 가져옴
            lookup_url = f'http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey={key}&itemIdType=ISBN13&ItemId={isbn13}&output=js&Version=20131101&OptResult=ebookList,usedList,reviewList&OptResult=ratinginfo'
            response = requests.get(lookup_url)
            data = json.loads(response.text)
            items = data.get('item', {})
            subInfo = items[0].get('subInfo', {})
            ratingInfo = subInfo.get('ratingInfo', {})
            ratingScore = ratingInfo.get('ratingScore', 0)
            ratingCount = ratingInfo.get('ratingCount', 0)
        else:
            ratingScore = 0
            ratingCount = 0
        
        author_obj = Author.objects.get(name=author)
        book = Book(
            title=title,
            author=author_obj,
            pubdate=pub_date,  # pub_date 변환이 필요할 수 있음
            description=description,
            sales_point=salesPoint,
            rating_score=ratingScore,
            rating_count=ratingCount,
            cover_url=cover,
            publisher=publisher,
            pricesales=price_sales,
            pricestandard=price_standard,
            best_duration=bestDuration,
            best_rank=bestRank,
            link=link
        )

        # 데이터베이스에 저장
        book.save()
        # 테스트 출력용
        # print(f"제목: {title}, 저자: {author_obj.name}, 출판사: {publisher}, 출판일: {pub_date}, 설명: {description}, 판매가: {price_sales}, 정가: {price_standard}, 판매 포인트: {salesPoint}, 평점: {ratingScore}, 평점 수: {ratingCount}, 표지 URL: {cover}, 베스트셀러 기간: {bestDuration}, 베스트셀러 순위: {bestRank}, 링크: {link}")


def update_all_authors():
    author_list = list(Author.objects.values_list('name', flat=True))
    try:
        for author in author_list:
            update_data(author)
            print(f'{author} 데이터 저장 완료')
    except Exception as e:
        print(f"Error updating authors: {e}")


def setup_scheduler():
    scheduler.add_job(update_all_authors, 'interval', days=1)
    scheduler.start()
    print('setup_scheduler 완료')
