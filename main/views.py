from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from charity_donation.settings import EMAIL_HOST_USER
from main.models import Donation, Institution, Category


class LandingPage(View):
    def get(self, request):
        institutions = Institution.objects.all().filter(categories_id=1)
        organizacje_pozarzadowe_list = Institution.objects.all().filter(categories_id=2)
        lokalne_zbiorki_list = Institution.objects.all().filter(categories_id=3)
        donations = Donation.objects.all()
        institutions_quantity = 0
        institutions_list = []
        bags_quantity = 0
        for donation in donations:
            bags_quantity += donation.quantity
        for donation in donations:
            if donation.institution_id not in institutions_list:
                institutions_list.append(donation.institution_id)
                institutions_quantity += 1


        return render(request, 'index.html',
                      {"bags_quantity": bags_quantity, "institutions_quantity": institutions_quantity,
                       'institutions': institutions, 'organizacje_pozarzadowe': organizacje_pozarzadowe_list,
                       'lokalne_zbiorki': lokalne_zbiorki_list})

    def post(self, request):
        subject = request.POST.get('surname')
        message = request.POST.get('message')
        send_mail(subject, message, EMAIL_HOST_USER, ['kamil955955@gmail.com'], fail_silently=False)
        return redirect('landing_page')


class AddDonation(View):
    def get(self, request):
        categories_list = Category.objects.all()
        institutions_list = Institution.objects.all()
        if request.user.is_authenticated:
            return render(request, 'form.html', {'categories': categories_list, 'institutions': institutions_list})
        else:
            return redirect('login')

    def post(self, request):
        quantity = request.POST.get("quantity")
        institution = request.POST.get("institutions")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone")
        city = request.POST.get("city")
        zip_code = request.POST.get("postcode")
        pick_up_date = request.POST.get("data")
        pick_up_time = request.POST.get("time")
        pick_up_comment = request.POST.get("more_info")
        user = request.user.id
        institution = Institution.objects.get(id=institution)
        donation = Donation.objects.create(quantity=quantity, institution=institution, address=address,
                                           phone_number=phone_number, city=city, zip_code=zip_code,
                                           pick_up_date=pick_up_date,
                                           pick_up_time=pick_up_time, pick_up_comment=pick_up_comment, user_id=user)
        donation.save()
        category = Category.objects.get(id=institution.categories_id)
        donation.categories.add(category)
        subject = request.POST.get('surname')
        message = request.POST.get('message')
        send_mail(subject, message, EMAIL_HOST_USER, ['kamil955955@gmail.com'], fail_silently=False)
        return redirect('form_confirmation')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user_list = User.objects.all()
        email = request.POST.get("email")
        password = request.POST.get("password")
        subject = request.POST.get('surname')
        message = request.POST.get('message')
        send_mail(subject, message, EMAIL_HOST_USER, ['kamil955955@gmail.com'], fail_silently=False)
        for user in user_list:
            if email == user.email:
                if password == password:
                    login(request, user)
                    return redirect("landing_page")
                else:
                    return redirect("register")


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        subject = request.POST.get('surname')
        message = request.POST.get('message')
        send_mail(subject, message, EMAIL_HOST_USER, ['kamil955955@gmail.com'], fail_silently=False)
        if password == password2:
            new_user = User.objects.create(username=email, first_name=name, last_name=surname, email=email,
                                           password=password)
            new_user.save()
            return redirect("login")


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('landing_page')


class Profile(View):
    def get(self, request):
        donations = Donation.objects.filter(user_id=request.user.id)
        return render(request, 'profile.html', {"donations": donations})

    def post(self, request):
        taken = request.POST.get("name")


class ProfileSettings(UpdateView):
    model = User
    template_name = 'settings.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('profile')


class SettingsCheck(View):
    def get(self, request):
        return render(request, 'profilecheck.html')

    def post(self, request):
        password = request.POST.get("password")
        password2 = request.POST.get('password2')
        if password == request.user.password:
            if password == password2:
                return redirect(f'/settings/{request.user.id}')
            pass
        pass


class PasswordChange(View):
    def get(self, request):
        return render(request, 'passwordcheck.html')

    def post(self, request):
        password0 = request.POST.get("password0")
        password1 = request.POST.get("password1")
        password2 = request.POST.get('password2')
        user = User.objects.get(id=request.user.id)
        if password0 == request.user.password:
            if password1 == password2:
                user.set_password(f'{password1}')
                user.save()
                return redirect('landing_page')
            pass
        pass


class FormConfirmation(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class Archive(View):
    def get(self, request, pk):
        return render(request, 'archive.html')

    def post(self, request, pk):
        donation = Donation.objects.get(id=pk)
        donation.is_taken = True
        donation.save()
        return redirect('profile')
