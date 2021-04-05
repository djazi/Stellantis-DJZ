# Generated by Django 3.1.7 on 2021-04-04 03:51

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
                ('Date', models.DateField(auto_now_add=True)),
                ('heure', models.TimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Map_Réference', models.CharField(max_length=50)),
                ('Map_Zone_Kit', models.CharField(max_length=50)),
                ('condiQ', models.IntegerField()),
                ('Designation_Produit', models.CharField(max_length=128)),
                ('Train', models.CharField(max_length=50)),
                ('nbr_Réf_Famille', models.IntegerField()),
                ('Point_De_consom', models.CharField(max_length=50)),
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
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GA_UEP.group')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GA_UEP.person')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(through='GA_UEP.Membership', to='GA_UEP.Person'),
        ),
    ]
