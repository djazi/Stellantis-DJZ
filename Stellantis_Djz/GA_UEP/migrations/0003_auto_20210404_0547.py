# Generated by Django 3.1.7 on 2021-04-04 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GA_UEP', '0002_auto_20210404_0518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventaire',
            name='Date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='inventaire',
            name='heure',
            field=models.TimeField(),
        ),
    ]
