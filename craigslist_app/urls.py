"""craigslist_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from craigslist.views import AnnouncementListView, AddAnnouncementView, CategoryAnnouncementView, LoginView, LogoutView, RegisterUserView, \
    UserAnnouncementView, AnnouncementUpdateView, AnnouncementDeleteView, UserProfileView, AnnouncementDetailView, ReservationCreateView,\
    UserReservationsView, TransactionCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AnnouncementListView.as_view(), name="index"),
    path('add-announcement/', AddAnnouncementView.as_view(), name="add-announcement"),
    path('announcement/<pk>/', AnnouncementDetailView.as_view(), name="announcement"),
    path('edit-announcement/<int:pk>', AnnouncementUpdateView.as_view(), name="edit-announcement"),
    path('delete-announcement/<int:pk>', AnnouncementDeleteView.as_view(), name="delete-announcement"),
    path('category/<int:category_id>', CategoryAnnouncementView.as_view(), name="category-announcement"),
    path('my-announcements', UserAnnouncementView.as_view(), name="my-announcements"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterUserView.as_view(), name="register"),
    path('my-profile/', UserProfileView.as_view(), name="my-profile"),
    path('book-announcement/', ReservationCreateView.as_view(), name="book-announcement"),
    path('my-reservations/', UserReservationsView.as_view(), name="my-reservations"),
    path('confirm/', TransactionCreateView.as_view(), name="confirm"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
