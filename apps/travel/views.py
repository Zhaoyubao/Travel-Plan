from django.shortcuts import render,  redirect
from ..login_register.models import User
from .models import Travel
from django.urls import reverse
from django.contrib import messages

def index(request):
    user = User.objects.get(id=request.session['user'])
    trips_user = Travel.objects.filter(user=user) | Travel.objects.filter(users=user).order_by('date_from', 'date_to')
    trips_others = Travel.objects.exclude(user=user).exclude(users=user).order_by('date_from','date_to')
    context = {
        'user' : user,
        'trips' : trips_user,
        'others' : trips_others
    }
    return render(request, 'travel/index.html', context)

def new(request):
    return render(request, 'travel/new.html')

def create(request):
    if request.method == 'POST':
        result = Travel.objects.validate_travel(request.POST)
        if result[0]:
            messages.success(request, result[1])
            return redirect(reverse('travel:index'))
        print_messages(request, result[1])
    return redirect(reverse('travel:new'))

def join(request, trip_id):
    u = User.objects.get(id=request.session['user'])
    trip = Travel.objects.get(id=trip_id)
    trip.users.add(u)
    messages.success(request, "Trip joined.")
    return redirect(reverse('travel:index'))

def cancel(request, trip_id):
    u = User.objects.get(id=request.session['user'])
    trip = Travel.objects.get(id=trip_id)
    trip.users.remove(u)
    messages.success(request, "Trip cancelled.")
    return redirect(reverse('travel:index'))

def delete(request, trip_id):
    Travel.objects.get(id=trip_id).delete()
    messages.success(request, "Trip deleted.")
    return redirect(reverse('travel:index'))

def show(request, trip_id):
    trip = Travel.objects.get(id=trip_id)
    other_users = trip.users.order_by('name')
    context = {
        'trip' : trip,
        'others' : other_users
    }
    return render(request, 'travel/show.html', context)

def print_messages(request, error_list):
     for error in error_list:
        messages.error(request, error)
