import json
import aiohttp
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asgiref.sync import sync_to_async
from pathlib import Path
from .models import Book, Author
from bs4 import BeautifulSoup
import time
from django.db import transaction
from playwright.async_api import async_playwright

# 상수 및 전역 변수
scheduler = AsyncIOScheduler()
BASE_DIR = Path(__file__).resolve().parent.parent

# 유틸리티 함수
def get_secret(key):
    with open(BASE_DIR / 'secrets.json') as f:
        secrets = json.load(f)
    try:
        return secrets[key]
    except KeyError:
        raise EnvironmentError(f"Set the {key} environment variable.")

# 동기 데이터베이스 작업
@sync_to_async
def get_link():
    return list(Book.objects.all().values_list('link', flat=True))

@sync_to_async
def check_book_exists():
    return Book.objects.exists()

@sync_to_async
def delete_all_books():
    Book.objects.all().delete()

@sync_to_async
def get_author_list():
    return list(Author.objects.values_list('name', flat=True))

@sync_to_async
def save_book(book):
    book.save()

@sync_to_async
def get_author(author_name):
    return Author.objects.get(name=author_name)

@sync_to_async
def update_book_purchase_data(link, purchase_data):
    try:
        with transaction.atomic():
            books = Book.objects.filter(link=link)
            if not books:
                print(f"No book found with link {link}.")
                return

            for book in books:
                book.age_gender_ratings = purchase_data
                book.save()
    except Exception as e:
        print(f"Error updating book with link {link}: {e}")

# 웹 스크래핑 함수
async def age_purchase_data(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(url, timeout=60000)  # 타임아웃을 60초로 증가
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
            await browser.close()
            return {}

        SCROLL_PAUSE_TIME = 1
        scroll = 0
        purchase_data = {}

        while True:
            try:
                element = await page.query_selector('.Ere_prod_graphwrap_a')
                if element:
                    print("Element found")  # 디버깅 출력
                    content = await element.inner_html()
                    soup = BeautifulSoup(content, 'html.parser')
                    data = soup.find_all('div', class_='per')
                    age = ['10대 여성', '10대 남성', '20대 여성', '20대 남성', '30대 여성', '30대 남성', '40대 여성', '40대 남성', '50대 여성', '50대 남성', '60대 이상 여성', '60대 이상 남성']

                    for i in range(0, len(age)):
                        purchase_data[age[i]] = float(data[i].text[:-1])
                    break
                else:
                    print("Element not found")  # 디버깅 출력
            except Exception as e:
                print(f"Error: {e}")

            scroll += 1500
            if scroll >= 13500:
                print("Reached maximum scroll limit")  # 디버깅 출력
                break
            await page.evaluate(f"window.scrollTo(0, {scroll});")
            await asyncio.sleep(SCROLL_PAUSE_TIME)

        await browser.close()
        print("Purchase data:", purchase_data)  # 디버깅 출력
        return purchase_data

# 비동기 함수
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def update_data(author, session):
    key = get_secret('TTB_KEY')
    search_url = f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={key}&Query={author}&QueryType=Author&MaxResults=20&start=1&SearchTarget=Book&output=js&Version=20131101"
    items = []
    
    while items == []:
        response_text = await fetch(session, search_url)
        try:
            data = json.loads(response_text)
            items = data.get('item', [])
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return

    print(f'{author} 검색 완료', len(items))

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
        
        if isbn13:
            lookup_url = f'http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey={key}&itemIdType=ISBN13&ItemId={isbn13}&output=js&Version=20131101&OptResult=ebookList,usedList,reviewList&OptResult=ratinginfo'
            response_text = await fetch(session, lookup_url)
            data = json.loads(response_text)
            items = data.get('item', {})
            subInfo = items[0].get('subInfo', {})
            ratingInfo = subInfo.get('ratingInfo', {})
            ratingScore = ratingInfo.get('ratingScore', 0)
            ratingCount = ratingInfo.get('ratingCount', 0)
        else:
            ratingScore = 0
            ratingCount = 0
        
        author_obj = await get_author(author)
        book = Book(
            title=title,
            author=author_obj,
            pubdate=pub_date,
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
            link=link,
        )

        await save_book(book)

async def update_all_authors():
    start_time = time.time()
    
    if await check_book_exists():
        await delete_all_books()
        print("모든 기존 데이터 삭제 완료")
    
    author_list = await get_author_list()
    
    async with aiohttp.ClientSession() as session:
        try:
            await asyncio.gather(*(update_data(author, session) for author in author_list))
        except Exception as e:
            print(f"Error updating authors: {e}")
    
    end_time = time.time()
    print(f"총 소요 시간: {end_time - start_time} 초")

async def update_book_age_purchase_data(batch_size=3):
    start_time = time.time()
    links = await get_link()
    
    if not links:
        print("No links found")  # 디버깅 출력
        return

    tasks = [age_purchase_data(link) for link in links]

    # 작업을 배치로 나누기
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i + batch_size]
        print(f'{i//batch_size + 1} 번째 배치 처리 중')
        
        # 배치를 비동기적으로 처리
        try:
            results = await asyncio.gather(*batch)
        except Exception as e:
            print(f"Error during batch processing: {e}")
            continue

        for link, purchase_data in zip(links[i:i + batch_size], results):
            if purchase_data:
                print(f"Link: {link}, Purchase Data: {purchase_data}")
                await update_book_purchase_data(link, purchase_data)
    
    end_time = time.time()
    print(f"연령별 구매 분포 데이터 업데이트: {end_time - start_time} 초")

# 스케줄러 설정
def setup_scheduler():
    scheduler.add_job(update_all_authors, 'interval', days=1)
    scheduler.add_job(update_book_age_purchase_data, 'interval', days=1)
    scheduler.start()
    print('setup_scheduler 완료')

# 메인 실행
if __name__ == "__main__":
    update_all_authors()
