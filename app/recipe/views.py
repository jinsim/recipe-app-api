# 우리가 만든 뷰는 단순히 뷰셋일 것임.
# 제네릭 뷰셋에 기초하여 list model mixin을 사용할 것이다.
# DRF의 특징으로, 뷰셋의 다른 기능은 가져오지 않고 우리가 사용할 list model function만 가져온다.
# 생성 삭제는 필요없고, 목록만 가져오면 됨.
# 이는 제네릭 뷰셋과 list model mixin의 조합으로 가능하다.
# 상태를 확인하여 커스텀 액션을 위한 상태를 만드는 목적
from rest_framework import viewsets, mixins, status
# 인증을 위해서
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# 뷰셋에 커스텀 액션을 추가하는데 사용됨.
from rest_framework.decorators import action
# 커스텀 response를 반환하기 위함.
from rest_framework.response import Response


from core.models import Tag, Ingredient, Recipe
from recipe import serializers

# Tag뷰셋과 ingredient뷰셋이 공통점이 많아, 합치도록 하겠다.
# 원하는 믹스인만 골라 넣으면 된다.
# CreateModelMixin을 추가하였으면 생성 옵션이 추가되므로 create func을 재정의할 수 있다.


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    # 상세한 기능을 덮어쓰고 싶으면 공식 문서 참고
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # 해당 뷰셋이 호출될 때, 객체를 검색하기 위해서 get_queryset함수를 호출할 것이다.
    # 우리는 이를 상속해서 인증된 유저만 가능하도록 제한할 수 있다.
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        # Tag.objects.all() 처럼 해도 되긴 하지만, 만약 해당 객체가 변경중일 때 검색하면 작업이 수행되지 않는다.
        # 이미 인증된 유저일 것이다.
        return self.queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()

    # 객체를 create할 때 자동으로 실행되는 함수이다.
    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    # 뷰셋으로 CRUD 기능을 커버
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""

        return self.queryset.filter(user=self.request.user)

    # 스펠링을 맞추지 않으면 작동하지 않을 수도 있다.
    # get serializer class로 serializer을 설정하는 것이 가장 좋다.
    # 이 방식으로 DRF는 browsable api 안에서 어떤 serializer를 보여줄 지 알 수 있다.
    def get_serializer_class(self):
        # 액션에 따라서 적합한 serializer을 반환한다.
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        # reciple의 user를 현재 요청하는 user로 설정한다.
        serializer.save(user=self.request.user)

    # 위의 get queryset, get serializer class, perform create는 디폴트 액션이다.
    # override를 안하면 그냥 디폴트 액션이 실행된다.
    # 우리는 여기에 커스텀 함수를 넣을 수 있다. 그리고 그것을 커스텀 액션으로 정의 가능하다.
    # method를 정의할 수 있다. 우리는 사용자가 이미지를 게시하도록 작업을 만들 것이니 post
    # detail을 true로 한 것은, 액션이 detail, 즉 세부 레시피를 위한 작업이라는 뜻.
    # 이미 존재하는 레시피에 대한 이미지만 업로드 가능.
    # url_path에 레시피의 id가 있는 세부 url을 넣어야한다.
    @action(methods=['POST'], detail=True, url_path='upload-image')
    # pk는 url과 함께 전달되는 primary key
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe"""
        # get object는 디폴트를 가져오거나 url의 id를 기반으로 접근 한 객체를 가져온다.
        recipe = self.get_object()
        # 레시피와 request.data를 넣어서 보냄.
        # get_serializer_class를 업데이트해야함.
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        # 데이터가 유효한지 확인함. 이미지가 있는지, 추가 필드는 없는지.
        if serializer.is_valid():
            # 모델 시리얼라이저를 쓰고 있음. save를 하면 객체가 저장됨.
            serializer.save()
            # Response를 반환함.
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        # serializer에 잘못된 데이터가 있는 경우.
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
