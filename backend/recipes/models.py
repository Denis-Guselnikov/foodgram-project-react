from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    """Ингредиенты для рецепта."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения ингредиента'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Tag(models.Model):
    """Тэги для рецептов."""

    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Название'
    )
    color = ColorField(
        unique=True,
        null=True,
        max_length=7,
        verbose_name='Цветовой HEX-код'
    )
    slug = models.SlugField(
        unique=True,
        null=True,
        max_length=256,
        verbose_name='slug тэга'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return f'{self.name} {self.id}'


class Recipe(models.Model):
    """Модель для рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
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
        through='IngredientRecipe',
        verbose_name='Ингридиенты',
        related_name='ingredients'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Тэг'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (в минутах)',
        default=0,
        validators=[MinValueValidator(1, 'Время приготовления должно быть больше 1 минуты.')]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'],
                name='unique_author_name'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.author}'


class IngredientRecipe(models.Model):
    """Количество ингридиентов в блюде."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Связанные ингредиенты'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='resipe_ingredient',
        verbose_name='в каких рецептах ингредиенты'
    )
    amount = models.IntegerField(
        verbose_name='Количество ингредиентов',
        default=0,
        validators=[MinValueValidator(1, 'Значение должно быть больше нуля.')]
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe}: {self.ingredient.name}'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )

    class Meta:
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shoppingcart'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил в избанное {self.recipe}'
