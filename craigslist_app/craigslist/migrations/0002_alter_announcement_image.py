# Generated by Django 4.0.2 on 2022-05-22 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('craigslist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='image',
            field=models.ImageField(upload_to='static/images/%Y/%m/%d'),
        ),
    ]
