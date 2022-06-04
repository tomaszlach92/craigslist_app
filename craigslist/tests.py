from multiprocessing.connection import Client

import pytest
from django.test import TestCase, Client
from django.urls import reverse
from craigslist.models import Announcement, Category
from django.contrib.auth.models import User as AppUser


def create_announcement(status, category):
    """
    Create announcement object.
    """
    category = Category.objects.get(category_name=category)
    user_who_added = AppUser.objects.get(username='test')

    return Announcement.objects.create(
        title='TEST',
        description='Test description',
        price=30000,
        category=category,
        user_who_added=user_who_added,
        status=status,
        image='staticfiles/2022/06/04/test.jpg'
    )


def create_test_user(username, password):
    """
    Create second test user.
    """
    return AppUser.objects.create_user(
        username=username,
        password=password
    )


class AnnouncementsIndexViewTests(TestCase):
    def setUp(self):
        """
        Set up data to test.
        """
        AppUser.objects.create_user(
            username='test',
            password='test'
        )
        Category.objects.create(
            category_name='Elektronika'
        )

    def test_no_announcements(self):
        """
        If no announcements with status == 2 exist, an appropriate message is displayed.
        """
        create_announcement(1, 'Elektronika')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak ogłoszeń.")

    def test_view_announcements(self):
        """
        Test view index page if announcements with status == 2 exist
        """
        create_announcement(2, 'Elektronika')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['announcements']), 1)
        self.assertContains(response, "Zobacz ogłoszenie")


class AnnouncementsDetailViewTests(TestCase):
    def setUp(self):
        """
        Set up data to test.
        """
        AppUser.objects.create_user(
            username='test',
            password='test'
        )
        Category.objects.create(
            category_name='Elektronika'
        )

    def test_announcement_status_new_detail(self):
        """
        Test resonse contains if announcement status == 1
        """
        announcement = create_announcement(1, 'Elektronika')
        response = self.client.get(reverse('announcement', args=(announcement.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Oczekuje na akceptacje")
        self.assertNotContains(response, "Zarezerwuj przedmiot u kupującego")

    def test_announcement_status_accepted_detail_not_login_user(self):
        """
        Test response contains if announcement status == 1 and user is not log in
        """
        announcement = create_announcement(2, 'Elektronika')
        response = self.client.get(reverse('announcement', args=(announcement.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aktualne")
        self.assertNotContains(response, "Zarezerwuj przedmiot u kupującego")

    def test_announcement_status_accepted_detail_user_login(self):
        """
        Test response contains if announcement status == 1 and user is log in
        """
        user = create_test_user('test1', 'test1')
        self.client.login(username=user.username, password='test1')
        announcement = create_announcement(2, 'Elektronika')
        response = self.client.get(reverse('announcement', args=(announcement.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aktualne")
        self.assertContains(response, "Zarezerwuj przedmiot u kupującego")


class AnnouncementsCategoryViewTests(TestCase):
    def setUp(self):
        """
        Set up data to test.
        """
        AppUser.objects.create_user(
            username='test',
            password='test'
        )
        Category.objects.create(
            category_name='Elektronika'
        )
        Category.objects.create(
            category_name='AGD'
        )

    def test_view_for_announcements_in_category(self):
        """
        Test view category announcements page.
        """
        create_announcement(2, 'Elektronika')
        create_announcement(2, 'AGD')
        response = self.client.get(reverse('category-announcement', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['announcements']), 1)
        self.assertContains(response, "Zobacz ogłoszenie")
        self.assertContains(response, "Lista ogłoszeń dla kategorii Elektronika")
        self.assertNotContains(response, "Lista ogłoszeń dla kategorii AGD")


class UserAnnouncementViewTest(TestCase):
    def setUp(self):
        """
        Set up data to test.
        """
        AppUser.objects.create_user(
            username='test',
            password='test'
        )
        Category.objects.create(
            category_name='Elektronika'
        )

    def test_not_logged_can_not_display_view(self):
        """
        Test not logged can't display my-announcements page.
        """
        create_announcement(2, 'Elektronika')
        response = self.client.get(reverse('my-announcements'))
        self.assertEqual(response.status_code, 302)

    def test_logged_can_display_view(self):
        """
        Test not logged can't display my-announcements page.
        """
        create_announcement(2, 'Elektronika')
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('my-announcements'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['announcements']), 1)
        self.assertContains(response, 'Lista Twoich wszystkich Twoich ogłoszeń')
