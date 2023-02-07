'''
from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world. You're at the ridesharing index.")
'''
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from .forms import RideSharerForm,EditOwnerForm,RideDropForm
from .models import RideOwner,RideSharer,Driver
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail

@login_required
def request_ride(request):
    if request.method == 'POST':
        # Get the form data
        destination = request.POST.get('destination')
        arrival_date_time = request.POST.get('arrival_date_time')
        number_passengers = request.POST.get('number_passengers')
        vehicle_type = request.POST.get('vehicle_type', '')
        special_requests = request.POST.get('special_requests', '')
        is_shared = request.POST.get('is_shared', False)
        is_shared = (is_shared == 'on')
        number_requested=number_passengers
        # Create a RideOwner object and save it to the database
        ride_owner = RideOwner(
            user=request.user,
            destination=destination,
            arrival_date_time=arrival_date_time,
            number_passengers=number_passengers,
            vehicle_type=vehicle_type,
            special_requests=special_requests,
            is_shared=is_shared,
            number_requested=number_requested
        )
        ride_owner.save()

        return redirect('home')
    else:
        return render(request, 'ridesharing/request_ride.html')
#it is used for programmer to display all the rideowners
@login_required
def search_result(request):
    #destination = request.GET.get('destination')
    #arrival_window_start = request.GET.get('arrival_window_start')
    #arrival_window_end = request.GET.get('arrival_window_end')
    #number_passengers = request.GET.get('number_passengers')

    rides = RideOwner.objects.all()
    context = {'rides': rides, 'number_passengers': 1}
    return render(request, 'ridesharing/search_result.html', context)


@login_required
def search_ride(request):
    if request.method == 'POST':
        form = RideSharerForm(request.POST)
        if form.is_valid():
            # get the data from the form
            destination = form.cleaned_data['destination']
            earliest_arrival = form.cleaned_data['earliest_arrival']
            latest_arrival = form.cleaned_data['latest_arrival']
            number_passengers = form.cleaned_data['number_passengers']

            # search for rides based on the user's preferences
            rides = RideOwner.objects.filter(
                destination=destination,
                arrival_date_time__range=(earliest_arrival, latest_arrival),
                #number_passengers__lte=number_passengers,
                is_shared=True,
                status='open'
            )
            context = {'rides': rides, 'number_passengers': number_passengers}
            # render the results
            return render(request, 'ridesharing/search_result.html', context)
    else:
        form = RideSharerForm()

    return render(request, 'ridesharing/search_ride.html', {'form': form})


"""
def join_ride(request, ride_id):
    #retrieve the object
    ride = get_object_or_404(RideOwner, pk=ride_id)
    if ride.status == 'open':
        ride.number_passengers += 1#####################################################################
        ride.save()
        sharer = RideSharer.objects.create(user=request.user, ride=ride)
        return render(request, 'ridesharing/join_confirm.html', {'ride': ride, 'sharer': sharer})
    else:
        return redirect('ridesharing:search_ride')
"""
@login_required
def join_ride(request, ride_id,number_passengers):

    ride = get_object_or_404(RideOwner, pk=ride_id)
    #if we joined before, then we cannot join again
    if RideSharer.objects.filter(user=request.user, destination=ride.destination,earliest_arrival=ride.arrival_date_time,latest_arrival=ride.arrival_date_time).exists():
        response = HttpResponse("<html><body><h1 style='font-size:30px;'>You have already joined this ride.</h1></body></html>")
        response.write("<button onclick='history.back()'>Go back</button>")
        return response
    #Have passed the paremeter in the search_result.html
    ride.number_passengers += number_passengers
    ride.save()
    #when we join the ride, the shared ride's earliest_arrival and latest_arrival
    #would both change to the rideowner's time 
    sharer = RideSharer.objects.create(ride_owner=ride,
                                        user=request.user,
                                        destination=ride.destination,
                                        earliest_arrival=ride.arrival_date_time,
                                        latest_arrival=ride.arrival_date_time,
                                        number_passengers=number_passengers)
    #sending email
    send_mail(
        'share ride order confirmed',  # 主題
        'Your sharer ride order confirmed',  # 訊息
        'rideshareouch@outlook.com',  # 寄件人的電子郵件地址
        [sharer.user.email],  # 收件人電子郵件地址列表
        fail_silently=False,  # 設置為 True 可以靜默忽略錯誤
    )
    return render(request, 'ridesharing/join_confirm.html', {'ride': ride})

#for driver
@login_required
def search_ride_driver(request):
    driver = Driver.objects.get(user_id=request.user.id)
    rides = RideOwner.objects.all().filter(status='open', 
                                           number_passengers__lte=driver.max_passengers, 
                                           vehicle_type=driver.vehicle_type)
    context = {'rides': rides}
    return render(request, 'ridesharing/search_result_driver.html', context)


@login_required
def take_ride(request, ride_id):

    ride = get_object_or_404(RideOwner, pk=ride_id)
    #if we joined before, then we cannot join again
    ride.status = 'confirmed'
    ride.driver_id=request.user.id
    ride.save()
    ride_sharers = RideSharer.objects.filter(ride_owner=ride)
     #sending email
    send_mail(
        'Order confirmed(ride owner)',  # 主題
        'You are ride owner and your order confirmed',  # 訊息
        'rideshareouch@outlook.com',  # 寄件人的電子郵件地址
        [ride.user.email],  # 收件人電子郵件地址列表
        fail_silently=False,  # 設置為 True 可以靜默忽略錯誤
    ) 
    send_mail(
        'Order confirmed(ride sharer)',  # 主題
        'You are ride sharer and your order confirmed',  # 訊息
        'rideshareouch@outlook.com',  # 寄件人的電子郵件地址
        [ride_sharer.user.email for ride_sharer in ride_sharers],  # 收件人電子郵件地址列表
        fail_silently=False,  # 設置為 True 可以靜默忽略錯誤
    )
    return render(request, 'ridesharing/driver_confirm.html', {'ride': ride})

@login_required
def search_driver_confirmorder(request):
    rides = RideOwner.objects.all().filter(status ='confirmed',driver_id = request.user.id)
    context = {'rides': rides}
    return render(request, 'ridesharing/search_ride_driver_confirmorder.html', context)

def ride_complete(request, ride_id):

    ride = get_object_or_404(RideOwner, pk=ride_id)
    #if we joined before, then we cannot join again
    ride.status = 'completed'
    ride.save()
    ride_sharers = RideSharer.objects.filter(ride_owner=ride)
    send_mail(
        'Order completed(ride owner)',  # 主題
        'You are ride owner and your order completed',  # 訊息
        'rideshareouch@outlook.com',  # 寄件人的電子郵件地址
        [ride.user.email],  # 收件人電子郵件地址列表
        fail_silently=False,  # 設置為 True 可以靜默忽略錯誤
    )
    send_mail(
        'Order completed(ride sharer)',  # 主題
        'You are ride sharer and your order completed',  # 訊息
        'rideshareouch@outlook.com',  # 寄件人的電子郵件地址
        [ride_sharer.user.email for ride_sharer in ride_sharers],  # 收件人電子郵件地址列表
        fail_silently=False,  # 設置為 True 可以靜默忽略錯誤
    )
    return render(request, 'ridesharing/driver_completed.html', {'ride': ride})
@login_required
def edit_ride_owner(request, ride_id):
    ride = RideOwner.objects.get(id=ride_id)
    prev_req=ride.number_requested
    if request.method == 'POST':
        form = EditOwnerForm(request.POST, instance=ride)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.number_passengers = ride.number_passengers+ride.number_requested-prev_req
            ride.save()
            #form.save()
            return redirect('My_ride')
    else:
        form = EditOwnerForm(instance=ride)
    status=ride.status
    return render(request, 'ridesharing/edit_ride.html', {'form': form,'status':status})


@login_required
def edit_ride_sharer(request, ride_id):
    ride_sharer = RideSharer.objects.get(id=ride_id)
    ride_owner = ride_sharer.ride_owner
    prev_share=ride_sharer.number_passengers
    if request.method == "POST":
        form = RideDropForm(request.POST, instance=ride_sharer)
        if form.is_valid():
            ride_sharer=form.save(commit=False)
            if form.cleaned_data['drop_ride']:
                ride_owner.number_passengers-=prev_share
                ride_owner.save()
                ride_sharer.delete()
                messages.success(request, 'Ride dropped successfully')
                return redirect('My_ride')
            else:
                
                ride_owner.number_passengers+=ride_sharer.number_passengers-prev_share
                ride_owner.save()
                form.save()
                messages.success(request, 'Ride updated successfully')
                return redirect('My_ride')
    else:
        form = RideDropForm(instance=ride_sharer)
    status=ride_owner.status
    return render(request, 'ridesharing/edit_ride_sharer.html', {'form': form,'status':status})


@login_required
def show_vehicle_info_owner(request, ride_id):
    
    ride = RideOwner.objects.get(id=ride_id)
    ride_sharers= ride.ridesharers.all()
    if ride.driver_id:
        driver = Driver.objects.get(user_id=ride.driver_id)
    else:
        driver=None
    context = {
        "vehicle": driver,
        "status":ride.status,
        "ride_owner":ride,
        "ride_sharers":ride_sharers
    }
    return render(request, "ridesharing/vehicle_info.html", context)
@login_required
def show_vehicle_info_sharer(request, ride_id):
    ride_sharer = RideSharer.objects.get(id=ride_id)
    ride=ride_sharer.ride_owner
    ride_sharers= ride.ridesharers.all()
    if ride.driver_id:
        driver = Driver.objects.get(user_id=ride.driver_id)
    else:
        driver=None
    #driver = Driver.objects.get(user_id=ride.driver_id)
    context = {
        "vehicle": driver,
        "status":ride.status,
        "ride_owner":ride,
        "ride_sharers":ride_sharers
    }
    return render(request, "ridesharing/vehicle_info.html", context)

