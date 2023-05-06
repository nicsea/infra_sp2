from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    @staticmethod
    def get_rating(obj):
        return None if obj.rating is None else round(obj.rating)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category',)
        model = Title


class TitleWriteSerializer(TitleSerializer):

    def save(self, **kwargs):
        new_fields = {}
        if 'genre' in self.initial_data:
            genres_list = []
            genres_slug_list = dict(self.initial_data).get('genre')
            for genre_slug in genres_slug_list:
                if not Genre.objects.filter(slug=genre_slug).exists():
                    raise ValidationError('Genre does not exist')
                genres_list.append(Genre.objects.get(slug=genre_slug))
            new_fields['genre'] = genres_list
        if 'category' in self.initial_data:
            category_slug = self.initial_data['category']
            if not Category.objects.filter(slug=category_slug).exists():
                raise ValidationError('Category does not exist')
            new_fields['category'] = Category.objects.get(slug=category_slug)
        super().save(**new_fields)


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        required=False,
        default=serializers.CurrentUserDefault()
    )
    title = SlugRelatedField(
        slug_field='id',
        read_only=True,
        required=False,
        default=None
    )

    class Meta:
        fields = ('id', 'text', 'title', 'author', 'pub_date', 'score')
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            author = self.context['request'].user
            title_id = self.context['request'].parser_context['kwargs'][
                'title_id']
            if Review.objects.filter(author=author,
                                     title__id=title_id).exists():
                raise serializers.ValidationError('Only one review is allowed')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'review', 'author', 'pub_date', 'text')
        read_only_fields = ['review']
        model = Comment
