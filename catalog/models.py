from django.db import models

class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Слаг', unique=True)


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField('Остаток', default=0)
    is_available = models.BooleanField('В наличии', default=True)

    image_path = models.CharField(
        'Путь к картинке',
        max_length=255,
        blank=True,
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title