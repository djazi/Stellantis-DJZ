# Generated by Django 3.1.7 on 2021-05-24 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GA_UEP', '0021_auto_20210524_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertes',
            name='SDate',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='inventaire',
            name='SDate',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
