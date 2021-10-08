import time

from django.db import connections
from django.db.utils import OperationalError
# 사용자 지정 명령을 생성하기위해 빌드해야하는 BaseCommnad
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    # 사용자 정의 인수와 옵션을 관리 명령에 전달. 대기 시간을 정의하거나 다른 옵션 사용 가능 
    def handle(self, *args, **options):
        # 관리 명령 중 실제로 출력 가능
        self.stdout.write('Waiting for database...')
        # 디비 연결을 나타내는 변수. 기본값은 None
        db_conn = None
        while not db_conn:
            try: 
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS('Datavase available!'))
