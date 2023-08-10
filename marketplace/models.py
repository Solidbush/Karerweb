from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = "Единица измерение"
        verbose_name_plural = "Единица измерении"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    desc = models.TextField(blank=True, null=True, verbose_name='Описание')
    category = models.ForeignKey(Category, models.PROTECT, verbose_name='Категория')
    unit = models.ForeignKey(Unit, models.PROTECT, verbose_name='Единица измерение')
    karer = models.ForeignKey("core.Karer", models.PROTECT, null=True)
    price = models.FloatField(null=True, verbose_name='Цена')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name
