from django.urls import path
from .views import request_ride,search_result,search_ride,join_ride, search_ride_driver,take_ride,ride_complete,search_driver_confirmorder,edit_ride_owner,edit_ride_sharer,show_vehicle_info_owner,show_vehicle_info_sharer
#from .views import RideRequestForm
urlpatterns = [
    #path('', views.index, name='index'),
     path('request_ride/', request_ride, name='request_ride'),
     path('search_result/',search_result,name='search_result'),
     path('search_ride/',search_ride,name='search_ride'),
     path('search_ride_driver/',search_ride_driver,name='search_ride_driver'),
     path('search_driver_confirmorder/',search_driver_confirmorder,name='search_driver_confirmorder'),
     #the ride_id is passed by the search_ride.html
     
     path('join_ride/ride_id=<int:ride_id>/share_num=<int:number_passengers>/', join_ride, name='join_ride'),
     path('take_ride/ride_id=<int:ride_id>/', take_ride, name='take_ride'),
     path('ride_complete/ride_id=<int:ride_id>/', ride_complete, name='ride_complete'),
    path('edit_ride_owner/ride_id=<int:ride_id>/', edit_ride_owner, name='edit_ride_owner'),
     path('edit_ride_sharer/ride_id=<int:ride_id>/', edit_ride_sharer, name='edit_ride_sharer'),
       path('show_vehicle_info_owner/ride_id=<int:ride_id>/', show_vehicle_info_owner, name='show_vehicle_info_owner'),
     path('show_vehicle_info_sharer/ride_id=<int:ride_id>/', show_vehicle_info_sharer, name='show_vehicle_info_sharer'),
     


]
