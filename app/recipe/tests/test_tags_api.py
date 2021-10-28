# 사용자 모델 가져오기
from django.contrib.auth import get_user_model
# URL 생성을 위한 reverse 가져오기
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Recipe
# unit 테스트를 작성한 후 통과시키기 위해서 시리얼라이저를 만든다.
from recipe.serializers import TagSerializer

# 이제 tag url을 만들 수 있다.
# 뷰셋을 사용하기 때문에 action name이 자동으로 url 끝에 추가된다. (라우터를 사용해서 -)
TAGS_URL = reverse('recipe:tag-list')

# public api test를 만들고, 로그인이 필요한 지 테스트해보자.


class PublicTagsApiTests(TestCase):
    """Test thje publicly available tags API"""

    def setUp(self):
        # 클라이언트 설정
        self.client = APIClient()

    # 태그를 검색하기 위해 로그인이 필요한지 검사한다.
    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)
        # 태그 api url에 인증되지 않은 요청을 할것임. 그러면 401이 반환
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# 인증된 사용자를 위한 testcase
class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        # 사용자 인증에 사용되는 user
        # 사용자 생성에 필요한 helper func를 만들어서 사용할 수도 있지만 별로 복잡하지 않아서 그냥 작성함.
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    # 샘플 태그를 몇 개 만들고, api 요청을 한 다음, 반환된 태그가 우리가 예상한 것과 같은지 확인.
    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        # db에서 이름 역순으로 저장되어있을 것이기 때문에.
        tags = Tag.objects.all().order_by('-name')
        # many=True속성을 넣지 않으면 단일 객체를 직렬화하는 것이라 가정함.
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # 인증된 유저가 만든 태그만 반환되는지 확인
    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        # 인증되지 않은 사용자 생성.
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    # tag가 성공적으로 만들어졌는지 확인.
    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)

        # 위 url에 payload를 post로 보내면 아래의 tag가 만들어져야한다.
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    # 잘못된 name을 가지고 payload를 만들 때.
    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # 쿼리 파라미터 assined_only를 True를 의미하는 1을 넣는다. 그럼 레시피에 할당된 태그만 반환된다.
    def test_retrieve_tags_assigned_to_recipes(self):
        """Test filtering tags by those assigned to recipes"""
        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Lunch')
        # 레시피를 만들어 tag1을 붙인다.
        recipe = Recipe.objects.create(
            title='Coriander eggs on toast',
            time_minutes=10,
            price=5.00,
            user=self.user
        )
        recipe.tags.add(tag1)

        # get에 딕셔너리를 함께 보냈다. assigned_only에 1. 쿼리 파라미터
        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_tags_assigned_unique(self):
        """Test filtering tags by assigned returns unique items"""
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        # 이걸 안만들면 무조건 len(res.data)가 1임.
        Tag.objects.create(user=self.user, name='Lunch')
        recipe1 = Recipe.objects.create(
            title='Pancakes',
            time_minutes=5,
            price=3.00,
            user=self.user
        )
        recipe1.tags.add(tag)
        recipe2 = Recipe.objects.create(
            title='Porridge',
            time_minutes=3,
            price=2.00,
            user=self.user
        )
        recipe2.tags.add(tag)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
