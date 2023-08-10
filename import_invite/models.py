import json
import uuid
from datetime import timedelta
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from simple_history.models import HistoricalRecords

from core.tasks import WAITING_PAY_NOTIFICATION


class BaseImport(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    karer = models.ForeignKey('core.Karer', models.PROTECT, verbose_name='Объект')
    desc = models.TextField(verbose_name='Описание')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    finish_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия')

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.id)


class OrgImport(BaseImport):
    organization = models.ForeignKey("core.Organization", models.PROTECT, verbose_name='Организация')

    class Meta:
        verbose_name = "Импорт юр. лицо"
        verbose_name_plural = "Импорты юр. лицо"


class BaseImportInvite(models.Model):
    STATUS = (
        ('waiting_pay', 'Ожидает оплаты'),
        ('payed', 'Оплачено'),
        ('finished', 'Успешно'),
        ('canceled', 'Отклонена')
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    product = models.ForeignKey("marketplace.Product", models.PROTECT, verbose_name='Продукт', null=True)
    car = models.ForeignKey("core.Car", models.PROTECT, verbose_name='Номер машины')
    driver = models.ForeignKey("core.Driver", models.PROTECT, verbose_name='Водитель')
    weight = models.FloatField(verbose_name='Потребность (кг)')
    status = models.CharField(max_length=255, choices=STATUS, default='waiting_pay', verbose_name='Статус')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    finish_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия')
    position = models.PositiveIntegerField(null=True, verbose_name='Позиция')

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.product)

    @classmethod
    def check_plate(cls, plate, karer_slug):
        return cls.objects.filter(
            car__number=plate, order__karer__slug=karer_slug
        ).order_by("position", "create_at").first()


class OrgImportInvite(BaseImportInvite):
    order = models.ForeignKey(OrgImport, models.CASCADE, verbose_name='Импорт')
    history = HistoricalRecords()

    class Meta:
        ordering = ['position']
        verbose_name = "Заявка юр. лицо"
        verbose_name_plural = "Заявкы юр. лицо"


def get_invite(invite_id):
    invite = OrgImportInvite.objects.filter(id=invite_id).first()
    return invite


@receiver(post_save, sender=OrgImportInvite)
def invite_schedules(sender, instance, created, **kwargs):
    if created:
        model_str = '.'.join((sender._meta.app_label, sender._meta.model_name))
        crontab, _ = CrontabSchedule.objects.get_or_create(hour=f"*/{WAITING_PAY_NOTIFICATION}")
        PeriodicTask.objects.create(
            name=str(uuid.uuid4()),
            task="notification_before",
            kwargs=json.dumps({'ids': [str(instance.id)], 'state': str(instance.status), "model_str": model_str}),
            start_time=timezone.now() + timedelta(hours=WAITING_PAY_NOTIFICATION),
            one_off=True, crontab=crontab,
            description=f"Уведамление юр. лица {instance.id}",
        )
