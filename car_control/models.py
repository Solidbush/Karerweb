from django.db import models


class History(models.Model):
    car = models.ForeignKey("core.Car", models.CASCADE, to_field='number', verbose_name='Машина')
    type = models.CharField(max_length=255, verbose_name="Тип собитие")
    mode = models.CharField(max_length=255, verbose_name='Собитие')
    date = models.DateTimeField(verbose_name='Дата и время')

    class Meta:
        verbose_name = "Контроль машин"
        verbose_name_plural = "Контроль машин"
