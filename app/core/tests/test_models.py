from django.test import TestCase
# 모델에서 직접 가져올 수 있지만, 프로젝트의 어떤 시점에서 모델을 변경하고 싶을 수 있으므로. 쉽게 변경할 수 있기 때문에
from django.contrib.auth import get_user_model

# test Class 생성 
class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        # 테스트 이메일
        email = "test@londonappdev.com"
        password = "123"
        user = get_user_model().objects.create_user(
            email = email, 
            password = password,
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