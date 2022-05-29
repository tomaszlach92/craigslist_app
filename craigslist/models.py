from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

STATUS = (
    (1, 'nowe'),
    (2, 'zaakceptowane'),
    (3, 'odrzucone'),
    (4, 'zarezerwowane'),
    (5, 'sprzedane')
)


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)

    @property
    def category(self):
        return "{}".format(self.category_name)

    def __str__(self):
        return self.category


class Announcement(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_who_added = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=1)
    image = models.ImageField(upload_to='staticfiles/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30, blank=True)
    street = models.CharField(max_length=30, blank=True)
    zip_code = models.CharField(max_length=6, blank=True)
    phone = PhoneNumberField(blank=True, null=True, unique=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Reservation(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    reserved_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservation")


class Transaction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
