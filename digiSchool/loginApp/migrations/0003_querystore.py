# Generated by Django 4.0.1 on 2022-03-17 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginApp', '0002_userdb_rollnumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datestamp', models.DateTimeField(auto_now_add=True)),
                ('queryAddress', models.EmailField(max_length=254)),
                ('queryurl', models.CharField(default=None, max_length=100)),
                ('queryContent', models.CharField(max_length=500)),
                ('resolve_status', models.BooleanField(default=False)),
            ],
        ),
    ]
