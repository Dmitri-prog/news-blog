from django.contrib.auth import get_user_model
from django.db import models

from blogicum.settings import LIMIT_MAX

User = get_user_model()


class BaseModel(models.Model):
    """Абстрактная модель. Описывает поле статуса публикации
    записи и время её создания."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    """Модель, описывающая категории публикаций. Кроме полей
    абстрактной модели содержит поля названия категорий публикаций,
    их описание и идентификатор каждой категории."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL;'
                  ' разрешены символы латиницы, цифры,'
                  ' дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        return self.title[:LIMIT_MAX]


class Location(BaseModel):
    """Модель, описывающая местоположения создания публикаций. Кроме полей
    абстрактной модели содержит поле названия местоположений публикаций."""

    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:LIMIT_MAX]


class Post(BaseModel):
    """Основная модель, описывающая сами публикации. Кроме полей
    абстрактной модели содержит следующие поля: название публикации,
    текст публикации, дата и время публикации, автор публикации (из
    встроенной модели User - связь N:1), категория публикации (из модели
    Category - связь N:1), местоположение публикации (из модели
    Location - связь N:1)."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем —'
                  ' можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    image = models.ImageField(
        'Фото',
        upload_to='posts_images',
        blank=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        return self.title[:LIMIT_MAX]


class Comment(models.Model):
    """Модель, описывающая комментарии к публикации. Содержит следующие поля:
    текст комментария, связанная публикация (из модели Post - связь N:1),
    автор комментария (из встроенной модели User - связь N:1),
    дата и время комментария."""
    text = models.TextField('Текст')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        default_related_name = 'comments'
        ordering = ('created_at', )
