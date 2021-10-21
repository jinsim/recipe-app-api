from django.test import TestCase
# 모델에서 직접 가져올 수 있지만, 프로젝트의 어떤 시점에서 모델을 변경하고 싶을 수 있으므로. 쉽게 변경할 수 있기 때문에
from django.contrib.auth import get_user_model

from core import models

# helper func을 추가해서 사용자를 생성함으로써 테스트에서 사용자를 쉽게 생성 가능
# sample_user와 함께 기본 옵션을 넣을 거임. 왜냐하면 대부분 우리가 사용하는 유저가 동일하기 때문에


def sample_user(email='test@londonappdev.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


# test Class 생성
class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        # 테스트 이메일
        email = "test@londonappdev.com"
        password = "123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "test@LONDONAPPDEV.COM"
        user = get_user_model().objects.create_user(email, '123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        # 메일 주소를 전달하지 않거나, 빈 문자열을 전달하거나, 값이 아닌 문자열을 전달하거나 등을 하면 에러 발생함
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123')

    def test_create_new_superuser(self):
        """Test creating new super user"""
        user = get_user_model().objects.create_superuser(
            "test@londonappdev.com",
            "123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # 태그를 만들고, 정확한 문자열 표현으로 변환되는지 확인
    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    # 재료를 만들고, 정확한 문자열 표현으로 변환되는지 확인
    def test_ingredient_str(self):
        """Test the ingredient string respresentation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)
