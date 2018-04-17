from django.shortcuts import render,redirect
from django.contrib import messages
from models import *
import bcrypt

# Create your views here.
def index(request):

    return render (request,'travel_buddy/index.html')

def login(request):
    errors = User.objects.valid_login(request.POST)
    if errors:
        for error in errors:
            messages.error(request,error)
        return redirect ('/')
    else:
        request.session['user'] = User.objects.get(username=request.POST['username']).name
        request.session['id'] = User.objects.get(username=request.POST['username']).id
        return redirect ('/dashboard')  

def register(request):
    errors = User.objects.valid_registration(request.POST)
    if errors:
        for error in errors:
            messages.error(request,error)
        return redirect ('/')
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(name = request.POST['name'], username = request.POST['username'], password = password)
        request.session['user'] = User.objects.last().name
        return redirect ('/dashboard')
        
def dashboard (request):
    context = {
        'trips': User.objects.get(name = request.session['user']).other_trips.all(),
        'others': Trip.objects.exclude(other__name = request.session['user']).all()
        }
    return render (request, 'travel_buddy/dashboard.html', context)

def logout (request):
    request.session.clear()
    return redirect ('/')

def show (request,id):
    creator = Trip.objects.get(id=id).user_id
    context = {
        'trips': Trip.objects.get(id=id).other.exclude(id=creator),
        'travel': Trip.objects.get(id=id)
        }
    return render (request, 'travel_buddy/trips.html', context)

def delete (request,id):
    return redirect ('/dashboard')

def join(request,id):
    this_user = User.objects.get(name = request.session['user'])
    this_trip = Trip.objects.get(id=id)
    this_trip.other.add(this_user)
    return redirect ('/dashboard')

def create (request):
    return render (request,'travel_buddy/create.html')

def new_trip (request):
    errors = Trip.objects.valid_trip(request.POST)
    if errors:
        for error in errors:
            messages.error(request,error)
        return redirect ('/travels/create')
    else:
        destination = request.POST['destination']
        description = request.POST['description']
        travel_from = request.POST['travel_from']
        travel_to = request.POST['travel_to']
        creator = User.objects.get( name = request.session['user'])
        Trip.objects.create(destination = destination, description = description, travel_from = travel_from, travel_to = travel_to, user = creator)
        this_trip = Trip.objects.last()
        this_trip.other.add(creator)
        return redirect ('/dashboard')  

 



