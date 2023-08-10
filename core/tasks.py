import json
import uuid
from datetime import timedelta

from celery import shared_task
from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask

WAITING_CANCEL = 6
WAITING_PAY_NOTIFICATION = 24 - WAITING_CANCEL
PAYED_NOTIFICATION = 24 * 30 - WAITING_PAY_NOTIFICATION
WAITING_PAY_NOTIFICATION_SUBJECT = "Cancel invite"
WAITING_PAY_NOTIFICATION_TEXT = "Cancel invite {instance_id}, Your invite will be cancel after {hours} hours"
PAYED_NOTIFICATION_SUBJECT = "Cancel invite payed"
PAYED_NOTIFICATION_TEXT = "Cancel invite {instance_id}, Your invite will be cancel after {hours} hours"
CANCELED_SUBJECT = "Canceled invite"
CANCELED_TEXT = "Cancel invite {instance_id}"


@shared_task(name='send_email')
def send_email(email, subject, text):
    send_mail(subject, text, settings.EMAIL_HOST_USER, [email])


def _notification_before(model_str, ids, state):
    model = apps.get_model(model_str)

    if ids:
        qs = model.objects.filter(id__in=ids, status=state).exclude(status__in=['finished', 'canceled'])
    else:
        qs = model.objects.filter(status=state).exclude(status__in=['finished', 'canceled'])
    for instance in qs:
        subject = WAITING_PAY_NOTIFICATION_SUBJECT if instance.status == "waiting_pay" else PAYED_NOTIFICATION_SUBJECT
        message = WAITING_PAY_NOTIFICATION_TEXT if instance.status == "waiting_pay" else WAITING_PAY_NOTIFICATION_TEXT
        send_email.delay(
            instance.order.user.email, subject,
            message.format(instance_id=instance.id, hours=WAITING_CANCEL)
        )
        crontab, _ = CrontabSchedule.objects.get_or_create(hour=f"*/{WAITING_CANCEL}")
        PeriodicTask.objects.create(
            name=str(uuid.uuid4()),
            task="cancel_invite",
            kwargs=json.dumps({'ids': [str(instance.id)], "state": state, "model_str": model_str}),
            start_time=timezone.now() + timedelta(hours=WAITING_CANCEL),
            one_off=True,
            crontab=crontab,
            description=message,
        )


def _cancel_invite(model_str, ids, state):
    model = apps.get_model(model_str)

    if ids:
        qs = model.objects.filter(id__in=ids).exclude(status__in=['finished', 'canceled'])
    else:
        qs = model.objects.exclude(status__in=['finished', 'canceled'])

    for instance in qs:
        if instance.status == state:
            send_email.delay(instance.order.user.email, CANCELED_SUBJECT, CANCELED_TEXT)
            instance.status = 'canceled'
            instance.save()
        else:
            if instance.status == 'payed':
                crontab, _ = CrontabSchedule.objects.get_or_create(hour=f"*/{PAYED_NOTIFICATION}")
                PeriodicTask.objects.create(
                    name=str(uuid.uuid4()),
                    task="notification_before_org",
                    kwargs=json.dumps({'ids': [str(instance.id)], 'state': instance.status, "model_str": model_str}),
                    start_time=timezone.now() + timedelta(hours=PAYED_NOTIFICATION),
                    one_off=True, crontab=crontab,
                    description=f"Уведамление юр. лица {instance.id} с 'ожидание оплаты' на 'отклонена'",
                )


@shared_task(name="notification_before")
def notification_before(model_str, ids, state):
    _notification_before(model_str, ids, state)


@shared_task(name="cancel_invite")
def cancel_invite(model_str, ids, state):
    _cancel_invite(model_str, ids, state)
