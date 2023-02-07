from django.urls import path

from .views import SignUpView,register_driver,My_ride,driver_info,Vehicle_info
from django.views.generic.base import TemplateView

urlpatterns = [
    #path("sign/", signupview, name="sign"),
    path("signup/", SignUpView, name="signup"),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('register_driver/', register_driver, name='register_driver'),
    path("My_ride/", My_ride, name="My_ride"),
    path('driver_info',driver_info,name='driver_info'),
    path("Vehicle_info/", Vehicle_info, name="Vehicle_info"),
]