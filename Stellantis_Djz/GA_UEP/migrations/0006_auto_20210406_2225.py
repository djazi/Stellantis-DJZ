# Generated by Django 3.2 on 2021-04-06 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GA_UEP', '0005_auto_20210406_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventaire',
            name='Date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='inventaire',
            name='Nombre_De_Bac',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='inventaire',
            name='Reference',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='inventaire',
            name='SM_Csc',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='inventaire',
            name='Zone_De_Kit',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='inventaire',
            name='heure',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
