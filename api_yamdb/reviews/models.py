from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import year_not_future

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Category name'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Unique adress'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Genre name'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Unique adress'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Title name'
    )
    year = models.IntegerField(
        verbose_name='Title year',
        validators=[year_not_future]
    )
    description = models.TextField(
        blank=True,
        verbose_name='Title description'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        through_fields=('title', 'genre'),
        verbose_name='Genre title'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Category title'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.name

    @property
    def rating(self):
        if hasattr(self, '_rating'):
            return self._rating


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Title'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Genre'
    )

    class Meta:
        ordering = ('-id',)
        unique_together = ('title', 'genre',)
        verbose_name = 'Genre title'
        verbose_name_plural = 'Genre titles'

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Title'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='User'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Publish date'
    )
    text = models.TextField('Text')
    score = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        verbose_name='Rating'
    )

    class Meta:
        ordering = ('-pub_date',)
        unique_together = ('title', 'author')
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Comment'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='User'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Publish date'
    )
    text = models.TextField('Text')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'{self.text} {self.author}'
