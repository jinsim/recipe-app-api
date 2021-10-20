# recipe-app-api
recipe-app-api source code

이 코드는 Udemy의 https://www.udemy.com/course/django-python-advanced/ 을 참고하여 작성되었다.
--

#### 서론
위 강의는 TDD를 사용하여 파이썬에서 REST API를 빌드하는 방법을 알려주는 강의이다. 
그 과정에서 Docker, Travis CI, Django REST Framework, Postgres DB, flake8을 사용하였다. 

#### 강의를 선택한 이유
우선, Docker와 CI CD에 관심이 있었고, 직접 서비스에 적용해볼 예정이라 쉽게 따라할 수 있는 강의로 결정하였다. 
또한, Django를 어느정도 개발해보았지만 깊게 파진 못했어서 Django 심화 버전을 공부해보고 싶었다. 

#### 강의 흐름
사용할 기술들에 대한 간략한 소개 -> 기술들을 설정하는 방법 소개 -> 개발
개발 내에서는 TDD 기법을 따라 test 폴더를 만들고, model을 테스트하고, model을 만들고, view를 테스트하고, view를 만들고... 
완성될 페이지나 api가 어떤 식으로 작업될지를 미리 결정하고 그것에 맞게 테스트를 만든 후, 테스트를 통과할 수 있도록 코드를 작성하였다.

#### 평가 
장점과 단점을 나눠서 평가하겠다. 
우선 평가 전에, 아래에 필자의 현재 상황을 기술하였으니 참고 바란다.
1. 영어 못함.
2. Django REST Framework로 서비스 개발 및 운영 경험 있음.
3. Mysql DB 사용 경험 있음.
4. Docker, Travis CI 경험 없음.
5. TDD 경험 없음.

###### 장점
