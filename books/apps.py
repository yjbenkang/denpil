import os
from django.apps import AppConfig
import threading
import time

class BooksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "books"
    initialization_event = threading.Event()

    def ready(self):
        # 현재 프로세스가 자동 리로더의 자식 프로세스인지 확인
        if os.environ.get('RUN_MAIN') != 'true':
            return

        # 초기화가 이미 완료되었으면 초기화 작업을 건너뜀
        if not BooksConfig.initialization_event.is_set():
            BooksConfig.initialization_event.set()
            threading.Thread(target=self.initialize_data, daemon=True).start()

    @staticmethod
    def initialize_data():
        # 데이터베이스 연결이 준비될 때까지 잠시 대기
        time.sleep(5)

        from django.db import connections
        from django.db.utils import OperationalError

        # 데이터베이스 연결 확인
        db_conn = connections['default']
        try:
            db_conn.cursor()
        except OperationalError:
            print("데이터베이스 연결 실패. 초기화를 건너뜁니다.")
            return

        # 데이터베이스 연결 이후 작업 수행
        from books.models import Author
        from .updater import update_all_authors, setup_scheduler
        update_all_authors()
        setup_scheduler()
        print("초기화 완료")
