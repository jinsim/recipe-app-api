# rest framework의 generics modules로 대체할 것임
# from django.shortcuts import render
from rest_framework import generics
# username과 password만 standard로 전달한다면, 해당 뷰에서 우리 url로 바로 토큰을 준다.
from rest_framework.authtoken.views import ObtainAuthToken
# api세팅
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    # renderer 클래스를 지정하면, 브라우저에서 검색가능한 api로 이 endpoint를 볼 수 있다.
    # 즉, 크롬이나 다른 것들을 통해 로그인할 수 있고, 이름과 암호를 입력가능하며, 포스트를 클릭하면 토큰이 반환되어야한다.
    # 이를 안할 거라면, C URL이나 다른 도구로 HTTP POST를 보내야한다.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
