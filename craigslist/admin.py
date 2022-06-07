from django.contrib import admin
from .models import Category, Announcement, Reservation, Transaction

admin.site.register(Category)
admin.site.register(Reservation)
admin.site.register(Transaction)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """
    Configure Announcement Admin view, add fields to display and field to filter by.
    """
    list_display = ('title', 'user_who_added', 'status', 'created_at', 'updated_at',)
    list_filter = ('status',)
