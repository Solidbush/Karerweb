from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .tasks import send_email
from .validators import INNCheckValidator

SEND_PVC_SUBJECT = "PVC"
SEND_PVC_TEXT = "Pvc for auth - {pvc}"


class Karer(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='Уникальная название', unique=True)
    address = models.TextField(blank=True, null=True, verbose_name='Адрес')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = "Объекты"


class Car(models.Model):
    number = models.CharField(max_length=100, verbose_name='Номер', unique=True)
    model = models.CharField(max_length=100, verbose_name='Модель')
    vin_number = models.CharField(max_length=100, verbose_name='Вин')
    model_seria = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"

    def __str__(self) -> str:
        return self.number


class Driver(models.Model):
    name = models.CharField(max_length=255, verbose_name='ФИО')
    phone = models.CharField(max_length=255, verbose_name='Номер телефона')

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"

    def __str__(self) -> str:
        return self.name


class Organization(models.Model):
    name = models.CharField("Название", max_length=255, blank=True)
    inn = models.CharField("ИНН", max_length=20, unique=True,
                           validators=[
                               MaxLengthValidator(10, 'Неправильный ИНН'),
                           ])
    bik = models.CharField("ВИК", max_length=255, blank=True)
    address = models.CharField("Адрес", max_length=255, blank=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    ogrn = models.CharField("ОГРН", max_length=20, blank=True)
    kpp = models.CharField("КПП", max_length=20, blank=True)

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self) -> str:
        return self.name

    def clean(self):
        validator = INNCheckValidator()
        org = validator(self.inn)
        self.address = org['a']
        self.name = org['c']
        self.ogrn = org['o']
        self.kpp = org['p']
        return super(Organization, self).clean()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        return super(Organization, self).save(force_insert, force_update, using, update_fields)


class Client(models.Model):
    name = models.CharField("ФИО", max_length=255)
    passport = models.CharField("Паспорт", max_length=20, unique=True)
    phone = models.CharField("Телефон", max_length=20, unique=True)

    class Meta:
        verbose_name = "Физическое лицо"
        verbose_name_plural = "Физическое лицо"

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    karer = models.ForeignKey(Karer, models.PROTECT, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True, error_messages={
        "unique": _("A user with that email already exists."),
    })
    is_staff = models.BooleanField(
        _("staff status"),
        default=True,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    password = models.CharField(_("password"), max_length=128, blank=True, null=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def send_pvc(self):
        from .utils import generate_pvc

        new_password = generate_pvc()
        self.set_password(new_password)
        self.save()
        send_email.delay(self.email, SEND_PVC_SUBJECT, SEND_PVC_TEXT.format(pvc=new_password))
