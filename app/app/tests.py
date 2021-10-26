# calc.py를 유닛테스트 하기 위한 파일.
# Django unit test framework는 tests로 시작하는 모든 파일을 찾는다.
# 기본적으로 이것들을 django run unit tests 명령어를 입력할 때 사용한다.
# 따라서 폴더나 파일 명이 tests 로 시작하는 것을 확인해야한다.

# 제일 먼저 할 일은, django test case를 import 하는 것이다.
from django.test import TestCase
# TestCase는 django 코드를 테스트할 때 도움이 되는 여러 함수들의 묶음이다.

# 우리가 테스트할 함수들을 import 한다.
from app.calc import add, subtract


# 우리가 만들고 싶은 테스트 클래스를 만들어준다.
class CalcTests(TestCase):
    # 항상 테스트하는 항목에 대한 설명으로 테스트를 시작한다.(미래의 유지보수를 위해)
    # 함수 이름에 대해서, 이런 함수들도 다 test로 시작해야한다. 안하면 실행되지 않음.
    def test_add_numbers(self):
        """Test that two numbers are added together"""
    # 테스트는 2가지 구성으로 되어있다.
    # setup(테스트하기 위해 함수를 설정하는)과 assertion(실제로 출력을 테스트하고 출력이 예상과 같은지 확인)
    # 여기서는 한 줄에 가능
        self.assertEqual(add(3, 8), 11)

    def test_subtract_numbers(self):
        """Test that values are subtracted and returned"""
        self.assertEqual(subtract(5, 11), 6)
