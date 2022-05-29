from django.contrib import admin
from .models import Category, Announcement, Reservation, Transaction

admin.site.register(Category)
admin.site.register(Announcement)
admin.site.register(Reservation)
admin.site.register(Transaction)
