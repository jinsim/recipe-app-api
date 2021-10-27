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
# jpeg-dev는 pillow때문. 
RUN apk add --update --no-cache postgresql-client jpeg-dev
# virtual이라는 옵션을 넣으면 종속성에 대한 별칭이 생성되므로 나중에 쉽게 종속성을 제거할 수 있다.
# 아래에 설치에 필요한 모든 임시 종속성을 나열해둔다. 알파인 이미지에 대한 완벽한 의존성임.
# musl~은 pillow때문. pipi페이지에서 찾았다. 권한 오류 없이 컨테이너 내에서 정적 및 미디어 파일을 저장할 수 있다.
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
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

# vol은 volume의 줄임말로, 하위 컨테이너에 다른 컨테이너와 공유해야하는 파일을 저장한다. 
# 이런 방식으로 컨테이너에서 볼륨 매핑이 필요한 위치를 모두 알 수 있따. 
# 예를 들어 이런 미디어 파일을 제공해야하는 nginx 또는 웹 서버가 있는 경우 
# 이 볼륨을 매핑하고 웹 서버 컨테이너와 공유해야한다.
RUN mkdir -p /vol/web/media
# django에는 정적 데이터를 저장하는 2개의 파일이 있다. 
# static은 js나 css같은 프로그램 실행 중에 변경되지 않는 서비스하려는 정적 파일
# media는 사용자에 의해 업로드되는 모든 미디어 파일. 여기서는 레시피 이미지.
RUN mkdir -p /vol/web/static
# 옵션으로 들어간 p는 모든 하위 디렉터리를 생성한다는 의미이다. 
# 즉, 기존에 vol이 없다면 vol, web, static까지 다 만든다.


# 도카를 사용하여 어플리케이션을 실행할 사용자를 만든다.
RUN adduser -D user

# 파일의 소유권을, 추가한 사용자로 이전할 것이다.
# 밑에 USER명령어로 사용자를 변경하기 전에 해야한다. 
# 그 이후에는 사용자가 파일을 직접 보거나 엑세스할 수 있는 권한을 부여하지 못한다. 
# vol 디렉터리 내의 모든 디렉터리의 소유권을 custom user에게 설정한다. 
# 옵션 R은 볼륨 권한을 설정하는 대신 볼륨 폴더의 하위 데럭터리를 설정한 것이다.
RUN chown -R user:user /vol/
# 소유자가 디렉터리로 모든 작업을 할 수 있고, 나머지는 디렉터리에서 읽고 쓸수 있다. 
RUN chmod -R 755 /vol/web


# 유저를 변경한다. 
USER user
# 이렇게 하는 이유는 보안을 위한 것. 이걸 하지 않으면, 이미지는 권장되지 않은 루트 계정을 사용하여 응용 프로그램을 실행한다. 누군가가 응용 프로그램을 손상시키면 전체 이미지에 대한 그룹 엑세스 권한을 갖게 되고 악의적인 작업 등을 할 수 있다. 
# 반면, 어플리케이션 전용 사용자를 별도로 만들면 공격자가 문서에 가지는 범위가 제한된다. 