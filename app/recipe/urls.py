from django.urls import path, include
# 뷰셋을 위한 url을 자동으로 생성하는 drf의 기능
# 따라서 뷰셋을 가지고 있을 때, 하나의 뷰셋과 연결된 여러 url을 가질 수 있다.
from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
# 뷰셋을 통해 특정 사용자에게 crud 작업같은 것을 할 때, 자동으로 url이 생성된다.

# 라우터에 뷰를 등록가능하다.
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    # 모든 요청을 전달해서 일치하는 경로로 전달할 것임.
    # 디폴트라우터를 통해 만들어진 모든 url이 url patterns에 포함된다.
    path('', include(router.urls))
]
