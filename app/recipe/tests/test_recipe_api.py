# 임시 파일을 생성할 수 있는 파이썬 함수
# 시스템 어딘가에 임시 파일을 생성하고 그 파일을 사용한 후 삭제까지 가능
import tempfile
# 경로 이름을 생성하고, 시스템에 파일이 있는지 확인하는 것들이 가능
import os

# PIL은 pillow requirement이자 원래 이름. pillow는 PIL의 fork이다. 현재 pillow가 권장됨.
# Image 클래스를 가져오면, 테스트 이미지를 생성해서 API에 업로드할 수 있다.
from PIL import Image


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def image_upload_url(recipe_id):
    # 업로드 이미지 url을 생성하는 함수.
    """Return URL for recipe image upload"""
    # 이미지를 업로드하기 위해서는 기존 레시피 id가 필요하다.
    # 따라서 reverse 함수에 인자로 넣는다.
    return reverse('recipe:recipe-upload-image', args=[recipe_id])


def detail_url(recipe_id):
    # api/recipes/id 에서 id가 항상 바뀌므로 list처럼 표준 url 설정이 힘듦.
    """Return recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name='Main course'):
    """Create and return a sample tag"""
    # 샘플 tag와 ingredient 객체를 생성하는 코드
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Cinnamon'):
    """Create and return a sample ingredient"""
    return Ingredient.objects.create(user=user, name=name)


def sample_recipe(user, **params):
    """Create and return a sample recipe"""
    # 테스트에서 반복적으로 객체가 필요할 때 도와주는 도우미 함수.
    # **params로 인해, 사용자가 추가로 전달한 모든 추가 매개변수가 params라는 사전으로 전달된다.
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    # 커스터마이징할 때 여기서 값을 바꾼다.
    defaults.update(params)
    # 이런 식으로 **dictionary하면 됨.
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test retrieving recipes for user"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'password123'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail"""
        recipe = sample_recipe(user=self.user)
        # n:n이라서 리스트에 추가하는 것임.
        # 2번째 인자를 비워서 디폴트 name이 들어감.
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    # 아무것도 안넣고 recipe 생성할 때 테스트
    def test_create_basic_recipe(self):
        """Test creating recipe"""
        # 생성할 때 넣을 정보들
        payload = {
            'title': 'Chocolate cheesecake',
            'time_minutes': 30,
            'price': 5.00
        }
        # HTTP post 요청 생성
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # 반환된 recipe가 우리가 생성할 때 넣은 정보들을 다 가지고 있는지 확인.
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            # getattr은 딕셔너리에서 key를 넣고 value를 가져옴
            self.assertEqual(payload[key], getattr(recipe, key))

    # 태그를 넣어서 recipe를 생성할 때 테스트
    def test_create_recipe_with_tags(self):
        """Test creating a recipe with tags"""
        tag1 = sample_tag(user=self.user, name='Vegan')
        tag2 = sample_tag(user=self.user, name='Dessert')
        # 태그를 생성해서 recipe에 넣는다.
        payload = {
            'title': 'Avocado lime cheesecake',
            # 태그를 넣는 것이 아니라 태그의 id를 넣음.
            'tags': [tag1.id, tag2.id],
            'time_minutes': 60,
            'price': 20.00
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        # 태그가 잘 들어간지 확인한다.
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        # assertIn은 리스트나 쿼리셋에서 객체가 있는지 확인할 때 주로 사용한다.
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    # 재료를 넣어서 recipe를 생성할 때 테스트
    def test_create_recipe_with_ingredients(self):
        """Test creating recipe with ingredients"""
        ingredient1 = sample_ingredient(user=self.user, name='Prawns')
        ingredient2 = sample_ingredient(user=self.user, name='Ginger')
        payload = {
            'title': 'Thai prawn red curry',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 20,
            'price': 7.00
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)

    # 업데이트에 대한 부분은 뷰셋 내장 기능이 있어 테스트를 만들지 않아도 된다.
    # 그러나 앱에서 사용할 모든 기능과 API 업데이트 방법을 보여주기 위해서 작성한다.
    def test_partial_update_recipe(self):
        # 부분 업데이트 - patch
        """Test updating a recipe with patch"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        new_tag = sample_tag(user=self.user, name='Curry')

        # title 과 tags 가 변경되고, 나머지는 그대로이다.
        payload = {'title': 'Chicken tikka', 'tags': [new_tag.id]}
        url = detail_url(recipe.id)
        self.client.patch(url, payload)

        # 모델에서 제공하는 db 새로고침 기능이다. 이걸 사용하지 않으면 값이 바뀌지 않는다.
        # 따라서 객체를 검색한 이후는 db가 바뀌더라도 refresh를 하지 않는 이상 바귀지 않는다.
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        tags = recipe.tags.all()
        # count로 객체 개수 세는 것과 동일함.
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_recipe(self):
        # 전체 업데이트 - put
        """Test updating a recipe with put"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        payload = {
            'title': 'Spaghetti carbonara',
            'time_minutes': 25,
            'price': 5.00
        }
        url = detail_url(recipe.id)
        self.client.put(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.price, payload['price'])
        # put에서는, payload에 제외한 부분은 삭제된다. 덮어쓰기이다.
        tags = recipe.tags.all()
        # payload에 없는 tag는 없어질 것이다.
        self.assertEqual(len(tags), 0)


class RecipeImageUploadTests(TestCase):
    # 이미지 업로드 함수들에는 몇가지 공통점들이 있으므로 클래스 분리함.

    # public private 말고 다른 클래스를 만들어도 됨. 상황에 따라 다른 setup 설정 필요.
    # setup 함수는 말 그대로, 테스트의 설정에서 일어나는 일들.
    # 테스트가 실행되기 전에 설정하고, 테스트가 끝난 후에는 사라지게 할 수 있음.(teardown)
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@londonappdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        # 테스트할 recipe도 고정으로 넣어버림.
        self.recipe = sample_recipe(user=self.user)

    # 테스트가 끝난 후에 시스템에 테스트 파일들이 쌓이는 것을 원치 않는다.
    def tearDown(self):
        self.recipe.image.delete()

    #
    def test_upload_image_to_recipe(self):
        """Test uploading an email to recipe"""
        url = image_upload_url(self.recipe.id)
        # suffix에 확장자를 넣을 수 있다.
        # ntf는 명명된 임시 파일의 줄임말. 이름 없이 파일을 반환하고 싶지 않기 때문에
        # 이름이 있어야 업로드 또는 이미지 업로드에서 create name func에 전달할 수 있다.
        # 우리가 쓸 수 있는 임시 파일을 시스템에 생성한 다음 컨텍스트 관리자를 종료.
        # 우리가 명령문을 벗어난 후에 자동으로 해당 파일을 제거.
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            # 이미지를 만드는 단계.
            # 10x10는 보이는 것이 중요한 것이 아니다.
            # 단위 테스트를 실행하기 위해 많은 메모리와 처리 능령
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            # 파이썬이 파일을 읽는 방식.
            # 파일을 저장했으므로, 끝점부터 다시 읽는다. 그래서 처음으로 재설정해줘야한다.
            ntf.seek(0)
            # multipart form으로 설정해야한다. 디폴트는 json.
            res = self.client.post(url, {'image': ntf}, format='multipart')

        # 데이터베이스 새로고침 후 제대로 값이 들어갔는지 확인
        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    # 잘못된 요청인 경우.
    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.recipe.id)
        # image의 경로가 실제로 존재하는지 확인 후, 잘못되었으면 오류를 발생시킨다.
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
