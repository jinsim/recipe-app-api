# core앱에 관리 명령을 추가할 것이다. 데이터베이스를 사용할 수 있을 때 까지 기다린 후 다른 명령을 수행하라는.
# postgres를 django에서 dockero compose와 함께 사용할 때,
# postgres가 준비가 되지 않은 상태에서 django 앱이 데이터베이스에 연결하려고 하면 에러가 발생한다.
# 따라서 프로젝트의 안정성을 향상시키기 위해서 docker compose에서 실행할 모든 명령 전에
# 이 도우미 명령을 추가하고, 데이터베이스에 엑세스 하기 전에 준비가 되었는지를 확인한다.

# 먼저, patch func. 이것을 통해 우리는 django get database function의 행동을 mock할 수 있다.
# 이렇게 하면 기본적으로 명령을 테스트할 때, 사용할 수 있는 데이터베이스와 사용할 수 없는 데이터베이스를 시뮬레이션 할 수 있다.
from unittest.mock import patch
# 밑에 call command function을 추가할 것이다. 소스코드의 호출을 허용해준다.
from django.core.management import call_command
# 여기서 데이터베이스를 사용할 수 없을 때 operation error을 가져온다. 이걸로 데이터베이스의 사용가능 여부를 테스트한다.
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    # 첫번째 기능은 단순히 명령을 호출하고 데이터베이스를 이미 사용할 수 있을 때 어떤 일이 일어나는지를 테스트한다.
    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # 여기서 테스트를 setup하려면, 데이터베이스가 사용가능할 때 django의 동작을 시뮬레이션해야한다.
        # 관리 명령어는 기본적으로 django에서 데이터베이스 연결을 검색하여 언제 데이터베이스 연결을 검색할 지 여부를 확인한다.
        # 따라서 테스트를 설정하기 위해 ConnectionHandler의 동작을 오버라이드할 것이다.
        # true 반환할 거고, exception을 반환하지 않을 것이다.

        # github에 djagno 코드가 있으니 참고하고, 여기서 실제로 호출되는 함수는 getitem이다.
        # patch를 사용함으로써, 우리가 지정한 값을 반환할 수도 있고, 몇번 호출되었는지 등 모니터링도 가능해진다.
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            # wait_for_db는 우리가 만들 management 명령의 이름
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    # db 명령을 기다리는 동안 데이터베이스가 5번 시도되고, 6번째일 때 성공한다.
    # patch 데코레이터를 걸어놓으면 실행할 때의 시간이 줄어듦.
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
