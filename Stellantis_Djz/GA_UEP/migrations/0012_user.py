# Generated by Django 3.1.7 on 2021-04-12 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GA_UEP', '0011_remove_person_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
