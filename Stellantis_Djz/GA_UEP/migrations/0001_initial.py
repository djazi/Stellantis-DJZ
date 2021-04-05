# Generated by Django 3.1.7 on 2021-04-05 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RU', models.CharField(max_length=50)),
                ('unite', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Inventaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Reference', models.CharField(max_length=50)),
                ('Nombre_De_Bac', models.IntegerField()),
                ('Zone_De_Kit', models.CharField(max_length=50)),
                ('Moniteur', models.CharField(max_length=50)),
                ('Date', models.DateField()),
                ('heure', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Map_Réference', models.CharField(blank=True, max_length=50, null=True)),
                ('Map_PDC', models.CharField(blank=True, max_length=50, null=True)),
                ('condiQ', models.IntegerField()),
                ('ligne', models.CharField(blank=True, max_length=50, null=True)),
                ('condi', models.CharField(blank=True, max_length=50, null=True)),
                ('UA_Appro', models.CharField(blank=True, max_length=50, null=True)),
                ('UcTourRef', models.FloatField()),
                ('Designation_Produit', models.CharField(blank=True, max_length=128, null=True)),
                ('Train', models.CharField(blank=True, max_length=50, null=True)),
                ('CVM', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('matricule', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Moniteur', models.CharField(max_length=50)),
                ('Ru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GA_UEP.group')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GA_UEP.person')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(through='GA_UEP.Membership', to='GA_UEP.Person'),
        ),
    ]
