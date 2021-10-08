# 파이썬 3.7 알파인을 상속받을 이미지로 설정한다.
FROM python:3.7-alpine
# 누가 유지 관리를 하는지 표현하는 코드이다.(선택)
MAINTAINER KBJ

# 도커 컨테이너 내에서 파이썬을 실행할 때 권장되는, 버퍼링되지 않는 모드에서 실행하도록 지시한다. - 도커 이미지와 같은 복잡한 문제를 피할 수 있다.
ENV PYTHONUNBUFFERD 1

# 의존성 설치
COPY ./requirements.txt /requirements.txt
# psycopg2 종속성때문에 설치
# 가장 작고 추가 종속성이 필요 없는 가장 좋은 방법
RUN apk add --update --no-cache postgresql-client
# virtual이라는 옵션을 넣으면 종속성에 대한 별칭이 생성되므로 나중에 쉽게 종속성을 제거할 수 있다.
# 아래에 설치에 필요한 모든 임시 종속성을 나열해둔다. 알파인 이미지에 대한 완벽한 의존성임.
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
# 우리가 삭제하려는 라인을 추가할 수 있다.
RUN apk del .tmp-build-deps


# 도커 이미지 내에 어플리케이션 소스 코드를 저장하는데 사용할 디렉터리를 만든다.
RUN mkdir /app
# 빈 폴더를 만들고, 그것을 기본 디렉터리로 전환한다.
# 도카 컨테이너를 사용하여 실행하는 모든 응용 프로그램은 별도로 지정하지 않는 한 이 위치에서 Stein을 실행한다. 
WORKDIR /app
# 로컬 컴퓨터에서 이미지에서 만든 앱 폴더를 앱에 복사한다. 
COPY ./app /app
# 이는 우리가 제품에서 미친듯이 사용하는 코드를 도켓의 이미지에 복사할 수 있게 해준다.

# 도카를 사용하여 어플리케이션을 실행할 사용자를 만든다.
RUN adduser -D user
# 유저를 변경한다. 
USER user
# 이렇게 하는 이유는 보안을 위한 것. 이걸 하지 않으면, 이미지는 권장되지 않은 루트 계정을 사용하여 응용 프로그램을 실행한다. 누군가가 응용 프로그램을 손상시키면 전체 이미지에 대한 그룹 엑세스 권한을 갖게 되고 악의적인 작업 등을 할 수 있다. 
# 반면, 어플리케이션 전용 사용자를 별도로 만들면 공격자가 문서에 가지는 범위가 제한된다. 