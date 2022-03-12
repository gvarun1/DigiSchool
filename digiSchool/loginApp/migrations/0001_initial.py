# Generated by Django 4.0.1 on 2022-03-12 07:45

import digiSchool.loginApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('email_addr', models.EmailField(max_length=254)),
                ('class_int', models.IntegerField()),
                ('class_section', models.CharField(max_length=1, validators=[digiSchool.loginApp.models.is_a_section])),
                ('school_name', models.CharField(max_length=100)),
                ('contact_detail', models.CharField(max_length=10, validators=[digiSchool.loginApp.models.is_a_number])),
                ('passwd', models.CharField(max_length=300)),
            ],
        ),
    ]
