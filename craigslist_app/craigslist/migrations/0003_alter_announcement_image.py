# Generated by Django 4.0.2 on 2022-05-22 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('craigslist', '0002_alter_announcement_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='image',
            field=models.ImageField(upload_to='images/%Y/%m/%d'),
        ),
    ]
