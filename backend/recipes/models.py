from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.db.models import UniqueConstraint

from .constants import (COLOR_REGEX, MAX_AMOUNT, MAX_COOKING_TIME,
                        MAX_HEX_COLOR_LENGTH, MAX_INGREDIENT_NAME_LENGTH,
                        MAX_MEASUREMENT_UNIT_LENGTH, MAX_RECIPE_NAME_LENGTH,
                        MAX_SLUG_LENGTH, MAX_TAG_NAME_LENGTH, MIN_AMOUNT_VALUE,
                        MIN_COOKING_TIME_VALUE)

User = get_user_model()


class Ingredient(models.Model):
    """Модель Ингридиентов."""

    name = models.CharField(
        'Название',
        max_length=MAX_INGREDIENT_NAME_LENGTH
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MAX_MEASUREMENT_UNIT_LENGTH
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель Тегов."""

    name = models.CharField(
        'Название',
        unique=True,
        max_length=MAX_TAG_NAME_LENGTH
    )
    color = models.CharField(
        'Цветовой HEX-код',
        unique=True,
        max_length=MAX_HEX_COLOR_LENGTH,
        validators=[
            RegexValidator(
                regex=COLOR_REGEX,
                message='Не является HEX цветом'
            )
        ]
    )
    slug = models.SlugField(
        'Уникальный слаг',
        unique=True,
        max_length=MAX_SLUG_LENGTH
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель Рецептов."""

    name = models.CharField(
        'Название',
        max_length=MAX_RECIPE_NAME_LENGTH
    )
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Автор',
    )
    text = models.TextField('Описание')
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME_VALUE,
                message=f'Время не может быть меньше {MIN_COOKING_TIME_VALUE}'
            ),

            MaxValueValidator(
                MAX_COOKING_TIME,
                message='Время приготовления должно быть '
                f'не более {MAX_COOKING_TIME} минуты!'
            )
        ]
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """Модель-связь ингридиентов и рецептов."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                MIN_AMOUNT_VALUE,
                message=f'Ингридиента не может быть меньше {MIN_AMOUNT_VALUE}'
            ),
            MaxValueValidator(
                MAX_AMOUNT,
                message=f'Максимальное кол-во должно быть {MAX_AMOUNT}'
            )
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return (
            f'{self.ingredient.name} ({self.ingredient.measurement_unit}) '
            f'- {self.amount} '
        )


class Favourite(models.Model):
    """Модель Избранного."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Избранное'


class ShoppingCart(models.Model):
    """Модель Корзины."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'
