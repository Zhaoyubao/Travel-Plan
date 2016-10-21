from django.shortcuts import render,  redirect
from ..login_register.models import User
from .models import Travel
from django.db.models import Count
from django.urls import reverse
from django.contrib import messages
from datetime import datetime

def index(request):
    user = User.objects.get(id=request.session['user'])
    users = User.objects.all()
    travels = Travel.objects.all()
    # trips = user.travel_set.all()
    trips = Travel.objects.filter(user=user)
    trips_joined = user.travels.all()
    others = Travel.objects.exclude(user=user)
    print '*'*70
    print "Users:", users.values('id', 'name', 'username')
    print "Trips:", travels.values('user', 'users', 'destination', 'plan', 'date_from', 'date_to')
    print '*'*70
    context = {
        'user' : user,
        'trips' : trips,
        'trips_joined' : trips_joined,
        'others' : others
    }
    return render(request, 'travel/index.html', context)

def new(request):
    return render(request, 'travel/new.html')

def create(request):
    if request.method == 'POST':
        result = validate_travel(request, request.POST)
        if result[0]:
            messages.success(request, result[1])
            return redirect(reverse('travel:index'))
        print_messages(request, result[1])
    return redirect(reverse('travel:new'))

def join(request, trip_id):
    u = User.objects.get(id=request.session['user'])
    trip = Travel.objects.get(id=trip_id)
    trip.users.add(u)
    return redirect(reverse('travel:index'))

def show(request, trip_id):
    u = User.objects.get(id=request.session['user'])
    trip = Travel.objects.get(id=trip_id)
    context = {
        'user' : u,
        'trip' : trip
    }
    return render(request, 'travel/show.html', context)


def print_messages(request, error_list):
     for error in error_list:
        messages.error(request, error)

def validate_travel(request, input):
    errors = []
    dest = input['destination']
    plan = input['plan']
    date_from = input['date_from']
    date_to = input['date_to']
    if not dest or dest.isspace():
        errors.append("Please enter the destination!")
    if not plan or plan.isspace():
        errors.append("Please enter the plan!")
    if not date_from:
        errors.append("Please select your travel date from!")
    if not date_to:
        errors.append("Please select your travel date to!")
    if date_from and date_to:
        date_delta = (datetime.now() - datetime.strptime(date_from, '%Y-%m-%d')).days
        trip_delta = (datetime.strptime(date_to, '%Y-%m-%d') - datetime.strptime(date_from, '%Y-%m-%d')).days
        if date_delta >= 0:
            errors.append("Travel dates should be future-dated!")
        if trip_delta < 0:
            errors.append('Travel date to should not be before the Travel date from!')

    if errors:
        return (False, errors)
    u = User.objects.get(id=request.session['user'])
    Travel.objects.create(destination=dest, plan=plan, date_from=date_from, date_to=date_to, user=u)
    return (True, "Trip added Successfully!")
