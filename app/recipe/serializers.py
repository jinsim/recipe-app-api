from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        # read_only_fields는 사용자가 request를 create or edit할 때 id를 업데이트하지 못하게 하기 위함이다.
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    # 관련 모델을 가져오기 위함이다. 1:N과 N:N 모델을 가져온다.
    # 재료에 대한 모든 것을 가져오는 것이 아니라, id만 가져오고 싶기 때문에 primarykeyrelatedfield를 넣는다.
    ingredients = serializers.PrimaryKeyRelatedField(
        # N:N이므로 many=True
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'ingredients', 'tags', 'time_minutes',
            'price', 'link'
        )
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    # 기존에 만든 RecipeSerializer을 상속한다.
    """Serialize a recipe detail"""
    # many=True로 인해 여러 재료들을 가질 수 있고, read_only=True로 인해 생성 및 변경할 수 없다.
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
