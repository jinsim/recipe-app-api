"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# media url을 설정하기 위함
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # url을 문자열로 정의하는 데 유용함
    path('api/user/', include('user.urls')),
    path('api/recipe/', include('recipe.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 개발 서버에서 media url을 사용할 수 있으므로 별도의 웹 서버를 설정하지 않고도 이미지 업로드를 테스트할 수 있다.
