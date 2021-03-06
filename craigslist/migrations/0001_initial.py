# Generated by Django 4.0.2 on 2022-05-22 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')
                 ),
                ('category_name',
                 models.CharField(max_length=64, unique=True)
                 ),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')
                 ),
                ('city', models.CharField(blank=True, max_length=30)),
                ('street', models.CharField(blank=True, max_length=30)),
                ('zip_code', models.CharField(blank=True, max_length=6)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(
                    blank=True, max_length=128, null=True, unique=True)
                 ),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('price', models.DecimalField(
                    decimal_places=2, max_digits=10
                )),
                ('status', models.IntegerField(
                    choices=[(1, 'new'), (2, 'accepted'),
                             (3, 'rejected'), (4, 'reserved'), (5, 'sold')
                             ],
                    default=1
                )),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='craigslist.category'
                )),
                ('user_who_added', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),
    ]
