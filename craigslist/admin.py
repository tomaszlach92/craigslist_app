from django.contrib import admin
from .models import Category, Announcement, Reservation

admin.site.register(Category)
admin.site.register(Announcement)
admin.site.register(Reservation)