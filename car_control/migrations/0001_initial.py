# Generated by Django 4.1 on 2023-04-14 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255, verbose_name='Тип собитие')),
                ('mode', models.CharField(max_length=255, verbose_name='Собитие')),
                ('date', models.DateTimeField(verbose_name='Дата и время')),
            ],
            options={
                'verbose_name': 'Контроль машин',
                'verbose_name_plural': 'Контроль машин',
            },
        ),
    ]
