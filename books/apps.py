import os
import asyncio
from django.apps import AppConfig
import threading
from asgiref.sync import sync_to_async

class BooksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "books"
    initialization_event = threading.Event()

    # def ready(self):
    #     # 현재 프로세스가 자동 리로더의 자식 프로세스인지 확인
    #     if os.environ.get('RUN_MAIN') != 'true':
    #         return
    #
    #     # 초기화가 이미 완료되었으면 초기화 작업을 건너뜀
    #     if not BooksConfig.initialization_event.is_set():
    #         BooksConfig.initialization_event.set()
    #         threading.Thread(target=self.run_async_initialization, daemon=True).start()
    #
    # @staticmethod
    # def run_async_initialization():
    #     asyncio.run(BooksConfig.initialize_data())
    #
    # @staticmethod
    # async def initialize_data():
    #     # 데이터베이스 연결이 준비될 때까지 잠시 대기
    #     await asyncio.sleep(5)
    #
    #     if not await BooksConfig.check_database_connection():
    #         print("데이터베이스 연결 실패. 초기화를 건너뜁니다.")
    #         return
    #
    #     # 데이터베이스 연결 이후 작업 수행
    #     from .updater import update_all_authors, setup_scheduler, update_book_age_purchase_data
    #     await update_all_authors()
    #     await update_book_age_purchase_data()
    #     setup_scheduler()
    #     print("초기화 완료")
    #
    # @staticmethod
    # @sync_to_async
    # def check_database_connection():
    #     from django.db import connections
    #     from django.db.utils import OperationalError
    #
    #     # 데이터베이스 연결 확인
    #     db_conn = connections['default']
    #     try:
    #         db_conn.cursor()
    #         return True
    #     except OperationalError:
    #         return False
