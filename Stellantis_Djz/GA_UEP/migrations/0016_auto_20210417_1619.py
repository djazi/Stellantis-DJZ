# Generated by Django 3.2 on 2021-04-17 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GA_UEP', '0015_alertes'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertes',
            name='Groupes',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='alertes',
            name='Shifts',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
