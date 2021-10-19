# 우리가 만든 뷰는 단순히 뷰셋일 것임.
# 제네릭 뷰셋에 기초하여 list model mixin을 사용할 것이다.
# DRF의 특징으로, 뷰셋의 다른 기능은 가져오지 않고 우리가 사용할 list model function만 가져온다. 생성 삭제는 필요없음. 목록만 가져오면 됨.
# 이는 제네릭 뷰셋과 list model mixin의 조합으로 가능하다.
from rest_framework import viewsets, mixins
# 인증을 위해서
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from recipe import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage tags in the database"""
    # 상세한 기능을 덮어쓰고 싶으면 공식 문서 참고
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # 이건 하나만 있는 것이 좋다.
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    # 해당 뷰셋이 호출될 때, 객체를 검색하기 위해서 get_queryset함수를 호출할 것이므로 우리는 이를 상속해서 인증된 유저만 가능하도록 제한할 수 있다.
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        # assigned_only = bool(
        #     int(self.request.query_params.get('assigned_only', 0))
        # )
        # queryset = self.queryset
        # if assigned_only:
        #     queryset = queryset.filter(recipe__isnull=False)

        # Tag.objects.all()해도 되긴 하지만, 만약 해당 객체가 변경중일 때 검색하면 작업이 수행되지 않는다.
        # 이미 인증된 유저일 것이다.
        return self.queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()
