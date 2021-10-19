# 앱에서 다른 경로를 지정할 수 있게 도와준다.
from django.urls import path

from user import views

# reverse 기능을 사용할 때 앱을 식별하는 용도
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),

]
