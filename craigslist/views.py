from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import FormView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.urls import reverse_lazy
from .forms import AnnouncementForm, LoginForm, RegisterUserForm, UserForm, ProfileForm
from .models import Announcement, Category, STATUS, Reservation
from django.contrib.auth.models import User as AppUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext as _

User = get_user_model()


class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'index.html'
    context_object_name = 'announcements'


class CategoryAnnouncementView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        announcements = Announcement.objects.filter(category_id=category_id)
        return render(request=request,
                      template_name="category_announcements.html",
                      context={
                          "category": category,
                          "announcements": announcements,
                      })


class UserAnnouncementView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        announcements = Announcement.objects.filter(user_who_added=user)
        return render(request=request,
                      template_name="user_announcements.html",
                      context={
                          "announcements": announcements,
                          "statuses": STATUS
                      })


class AddAnnouncementView(LoginRequiredMixin, FormView):
    template_name = 'form.html'
    success_url = reverse_lazy('index')
    form_class = AnnouncementForm

    def form_valid(self, form):
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        price = form.cleaned_data['price']
        category = form.cleaned_data['category']
        user_who_added = self.request.user
        image = form.cleaned_data['image']
        Announcement.objects.create(
            title=title,
            description=description,
            price=price,
            category=category,
            user_who_added=user_who_added,
            image=image,
        )
        messages.add_message(self.request, messages.SUCCESS, _('Ogłoszenie zostało dodane'))
        redirect_site = super().form_valid(form)
        return redirect_site


class AnnouncementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    success_url = reverse_lazy('my-announcements')
    template_name_suffix = '_update_form'

    def test_func(self):
        obj = self.get_object()
        return obj.user_who_added == self.request.user


class AnnouncementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Announcement
    success_url = reverse_lazy('my-announcements')

    def test_func(self):
        obj = self.get_object()
        return obj.user_who_added == self.request.user


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login_form.html', {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, _('Zalogowano poprawnie!'))
                return redirect('index')
            else:
                form.add_error(None, 'Niepoprawny login lub hasło')

        context = {
            'form': form
        }
        return render(request, 'login_form.html', context)


class AnnouncementDetailView(DetailView):
    model = Announcement


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, _('Wylogowano z systemu!'))
        return redirect('index')


class RegisterUserView(FormView):
    template_name = 'form.html'
    success_url = reverse_lazy('index')
    form_class = RegisterUserForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        AppUser.objects.create_user(
            username=username,
            password=password
        )
        redirect_site = super().form_valid(form)
        messages.add_message(self.request, messages.SUCCESS,
                             _('Zostałeś zarejestrowany! Zaloguj się by móc dodawać ogłoszenia!'))
        return redirect_site


class UserProfileView(View):
    def get(self, request):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.add_message(request, messages.SUCCESS, _('Profil zaaktualizowany!'))
            return redirect('my-profile')
        else:
            messages.add_message(request, messages.WARNING, _('Popraw błędy w formularzu'))
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })


class ReservationCreateView(LoginRequiredMixin, View):
    def post(self, request):
        announcement_id = request.POST['announcement_id']

        announcement = Announcement.objects.get(pk=announcement_id)
        announcement.status = 4
        announcement.save()

        Reservation.objects.create(
            announcement=announcement,
            reserved_by_user=self.request.user,
        )

        messages.add_message(request, messages.SUCCESS,
                             _('Przedmiot zarezerwowany u sprzedającego! Skontaktuj się z nim w celu realizacji transakcji'))
        return redirect('index')

class UserReservationsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        reservations = Reservation.objects.filter(reserved_by_user=user)
        return render(request=request,
                      template_name="user_reservations.html",
                      context={
                          "reservations": reservations
                      })