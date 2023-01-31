from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        required=True,
        max_length=150,
        regex=r'^[\w.@+-]+\Z',
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
    )

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User
        read_only_field = ('role',)


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User
        max_length = (150,)
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):
    """Сериализация регистрации пользователя и создания нового."""
    username = serializers.SlugField(
        max_length=150,
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if User.objects.filter(
                username=data['username'],
                email=data['email']).exists():
            return data
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем существует.'
            )
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email существует.'
            )
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username']
        )
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )
        lookup_field = 'slug'


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
        required=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True,
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True,
    )
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True,
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(min_value=1, max_value=10)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, attrs):
        if not self.context['request'].method == 'POST':
            return attrs
        if Review.objects.filter(
            title_id=self.context['view'].kwargs.get('title_id'),
            author=self.context['request'].user,
        ).exists():
            raise serializers.ValidationError(
                ('Попытка оставить повторный отзыв'),
            )
        return attrs
