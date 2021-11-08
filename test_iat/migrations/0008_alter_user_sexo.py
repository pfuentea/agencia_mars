# Generated by Django 3.2.5 on 2021-11-07 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_iat', '0007_alter_sondeo_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sexo',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro'), ('N', 'Ninguno')], default='N', max_length=2),
        ),
    ]