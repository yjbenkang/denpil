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
    url = f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={key}&Query={author}&QueryType=Author&MaxResults=100&start=1&SearchTarget=Book&output=js&Version=20131101"
    response = requests.get(url)
    data = json.loads(response.text)

    # 데이터 전처리
    items = data.get('item', [])
    print(len(items))
    for item in items:
        title = item.get('title', '')
        # author_name = item.get('author', '')
        pub_date = item.get('pubDate', '')
        description = item.get('description', '')
        salesPoint = item.get('salesPoint', 0)
        ratingScore = item.get('ratingScore', 0)
        ratingCount = item.get('ratingCount', 0)
        cover = item.get('cover', '')
        publisher = item.get('publisher', '')
        price_sales = item.get('priceSales', 0)
        price_standard = item.get('priceStandard', 0)
        bestDuration = item.get('bestDuration', '')
        bestRank = item.get('bestRank', 0)
        link = item.get('link', '')
        
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
        # print(title, author_name, publisher, pub_date, description, price_sales, price_standard, cover)


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


# 테스트 실행용
if __name__ == "__main__":
    author_list = ['가오싱젠', 'V. S. 나이폴', '임레 케르테스', 'J. M. 쿳시', '엘프리데 옐리네크', '해롤드 핀터',
                   '오르한 파묵', '도리스 레싱', 'J.M.G. 르 클레지오', '헤르타 뮐러', '마리오 바르가스 요사', '토마스 트란스트뢰메르', '모옌', '앨리스 먼로',
                   '파트릭 모디아노',
                   '스베틀라나 알렉시예비치', '밥 딜런', '가즈오 이시구로', '올가 토카르추크', '페터 한트케', '루이즈 글릭', '압둘라자크 구르나', '아니 에르노', '욘 포세',
                   '한강']

    update_all_authors(author_list)  # 최초 데이터 수집
    setup_scheduler(author_list)  # 1일 단위로 스케줄에 추가
    print(BASE_DIR)
    scheduler.start()
