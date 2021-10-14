from django.test import TestCase
# 테스트에 유저 모델이 필요해서
from django.contrib.auth import get_user_model
# API url을 만듦.
from django.urls import reverse

# API에 요청을 보낼 test client를 만들어준다.
from rest_framework.test import APIClient
# status code를 위해서
from rest_framework import status


# 값이 변하지 않는 변수를 뜻함.
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (piblic)"""

    def setUp(self):
        # 클라이언트를 계속 만들 필요 없이 재사용 가능. 편함.
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload successful"""
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        # 응답의 상태 코드가 200인지
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # 객체가 실제로 만들어졌는지
        # **은 딕셔너리 언패킹
        user = get_user_model().objects.get(**res.data)
        # 비번이 맞는지 확인
        self.assertTrue(user.check_password(payload["password"]))
        # 잠재적인 보안 취약점이므로 항상 비번을 보여주지 않도록 확인
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creatinga  user that already exists fails"""
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'Test',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'pw',
            'name': 'Test',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        # 이미 만들었는데 그럼 중복에서 걸리지 않나? 안걸림. 모든 테스트는 데이터베이스를 새로 고치기 때문에.
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    # 토큰을 만들 것임. 이제 request를 보낼 때 아이디와 비번을 보내는 것이 아니라 토큰으로 인증을 할 수 있음.
    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        # token이라는 키 값이 response에 있는지 확인한다.
        # 우리는 장고 내장 인증 시스템을 이용할 것이므로, 토큰 키에는 토큰 값이 있을것이다. 이는 생략한다.
        self.assertIn('token', res.data)
        # 요청이 성공한지 확인한다.
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # 잘못된 자격 증명을 제출할 경우. 토큰을 생성하지 않는다.
    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        # 사용자를 만들고, 일부러 잘못된 비밀번호를 준다.
        create_user(email='test@londonappdev.com', password="testpass")
        payload = {'email': 'test@londonappdev.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        # 토큰이 res 데이터에 없어야하고, 400 코드가 반환되어야한다.
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # 사용자가 없으면 토큰이 생성되지 않는지 테스트한다.
    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        # 테스트가 진행될때마다 데이터베이스는 초기화되므로, 위에서 같은 메일과 비번을 사용한 것은 중요하지 않다.
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # 누락된 경우.
    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
