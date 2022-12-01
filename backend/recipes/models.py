from django.db import models
from django.core.validators import MinValueValidator

from users.models import User


class Ingredient(models.Model):
    """Ингридиенты для рецепта."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название ингридиента'
    )
    measurement_unit = models.CharField(
        max_length=256,
        verbose_name='Единица измерения ингридиента'        
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Tag(models.Model):
    """Тэги для рецептов."""

    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Название'
    )
    color = models.CharField(
        unique=True,
        max_length=7,
        verbose_name='Цветовой HEX-код'
    )
    slug = models.SlugField(
        unique=True,
        max_length=256,
        verbose_name='slug тега'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель для рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name='recipes', 
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=256, 
        verbose_name='Название Рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение'
    )
    text = models.TextField(
        verbose_name='Описание Рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='AmountIngredient',
        verbose_name='Ингридиенты'
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
    )
    pub_date = models.DateTimeField(        
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        default=0,
        validators=(
            MinValueValidator(
                1,'Время приготовления не может быть меньше 1!'
            )            
        )
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class AmountIngredient(models.Model):
    """Количество ингридиентов в блюде."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_resipe',
        verbose_name='Связанные ингредиенты'
    )
    resipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='resipe_ingredient',
        verbose_name='В каких рецептах ингредиенты'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиентов',
        default=0,
        validators=(
            MinValueValidator(
                1, 'Нужно больше ингредиентов!'
            )
        )
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Количество ингридиентов'
        ordering = ['recipe']

    def __str__(self):
        return f'{self.resipe}: {self.ingredient.name}' 
