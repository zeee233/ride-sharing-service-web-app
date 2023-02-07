from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth.decorators import login_required

from .forms import DriverForm
'''
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    #for all generic class-based views the urls are not loaded when the file is imported
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
#class LogInView(generic.CreateView):
#    template_name = 'registration/login.html'
'''
"""
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'You account have already created. You can login now!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from ridesharing.models import Driver, RideOwner, RideSharer
from accounts.forms import CustomUserCreationForm


def SignUpView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data.get('email')
            user.save()
            # Log the user in
            login(request, user)
            # Redirect to a success page
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def register_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            user = request.user
            driver, created = Driver.objects.update_or_create(
                user=user,
                defaults={
                    'name':user.username,
                    'vehicle_type':form.cleaned_data['vehicle_type'],
                    'license_plate_number':form.cleaned_data['license_plate_number'],
                    'max_passengers': form.cleaned_data['max_passengers'],
                    'special_vehicle_info':form.cleaned_data['special_vehicle_info'],
                }
            )
            driver.save()
            return redirect('home')        
    else:
        form = DriverForm()
    return render(request, 'page/register_driver.html', {'form': form})

@login_required
def My_ride(request):
    rideOwner = RideOwner.objects.all().filter(user=request.user)
    rideSharer = RideSharer.objects.all().filter(user=request.user)
    return render(request, 'page/My_ride.html', {'rideOwner': rideOwner, 'rideSharer': rideSharer})

@login_required
def driver_info(request):
    try:
        driver = Driver.objects.get(user=request.user)
    except Driver.DoesNotExist:
        driver = None
    return render(request, 'page/driver_info.html', {'driver': driver})


def Vehicle_info(request):
    return render(request, 'page/Vehicle_info.html')
