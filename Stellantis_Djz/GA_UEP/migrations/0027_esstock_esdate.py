# Generated by Django 3.2.5 on 2021-07-06 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GA_UEP', '0026_auto_20210705_0359'),
    ]

    operations = [
        migrations.AddField(
            model_name='esstock',
            name='ESDate',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
