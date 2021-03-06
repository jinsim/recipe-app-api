# 모델 시리얼라이저를 만드려면 모델이 필요함
from django.contrib.auth import get_user_model, authenticate
# 번역을 위해서 필요함. 언어 파일을 쉽게 추가할 수 있고 자동으로 변환시킬 수 있다.
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        # 유저 모델을 반환한다.
        model = get_user_model()
        # HTTP POST를 만들 때, 시리얼라이저에 포함할 필드 지정.
        # 읽기 쓰기를 위해 API에 엑세스 할 수 있도록
        fields = ("email", "password", "name")
        # extra keyword args. 제한사항 걸기. 암호가 5자 이상인지 확인용.
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # 생성을 재정의함
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        # 그냥 create하면 안되고, model의 create_user가 실행 되어야 비번이 숨겨짐.
        return get_user_model().objects.create_user(**validated_data)

    # 업데이트를 재정의함. 객체와 검증된 데이터가 있어야한다.
    # instance는 modelserializer과 연결되어 user객체가 된다.
    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        # validated_data에서 비번을 제외함
        # 두번째 인자는 기본값.get과 달리 없으면 기본값을 제공해야함.
        password = validated_data.pop('password', None)
        # 나머지 validated_data에 대해 업데이트를 요청함
        # super을 사용하면 modelserializer의 update함수를 가져올 수 있다.
        # 이처럼 기본 기능을 가져와서 확장할 수 있다.
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        # 비번에 공백이 포함되었으면 좋겠다.
        trim_whitespace=False
    )

    # input이 정확한지, 유효한지 검사. 오버라이딩
    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
