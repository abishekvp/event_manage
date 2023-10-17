from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404
from .models import Image


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient("mongodb://localhost:27017", server_api=ServerApi('1'))

db_users = client.eventschedule.users
schedule = client.eventschedule.schedule


def updateschedule(request):
    event_id = request.POST.get("event_id")
    schedule.find_one_and_delete(filter={"event_id":event_id})
    return redirect('viewschedule')


def addschedule(request):
    if request.user.is_authenticated:
        if request.method == "POST" and "stage_image" in request.FILES:
            email = request.user.email
            print(email)
            date = request.POST["date"]
            client_name = request.POST["client_name"]
            function_place = request.POST["function_place"]
            function_name = request.POST["function_name"]
            stage_name = request.POST["stage_name"]
            stage_image = request.FILES["stage_image"]
            stage_image = Image(image=stage_image)
            stage_image.save()
            description = request.POST["description"]
            t_amount = request.POST["t_amount"]
            advance = request.POST["advance"]
            balance = request.POST["balance"]
            event_id = str(email+date+(str(client_name).replace(" ",""))+str(function_name).replace(" ","")).lower()
            print(event_id)
            schedule.insert_one({"email":email,"date":date, "client_name":client_name, "function_place":function_place, "function_name":function_name, "description":description, "stage_name":stage_name, "t_amount":t_amount, "advance":advance, "balance":balance, "event_id":event_id})
        return render(request, 'components/addschedule.html')
    else:return redirect('signin')

def viewschedule(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            event_id = request.POST["event_id"]
            schedule.find_one_and_delete(filter={"event_id":event_id})
        schedules = {}
        j=1
        for i in schedule.find(filter={"email":request.user.email}):
            schedules[j]=i
            j+=1
        return render(request, './components/viewschedule.html', {"schedules":schedules})
    else:return redirect('signin')

def index(request):
    if request.user.is_authenticated:return redirect("dashboard")
    else:return redirect('signin')

def dashboard(request):
    if request.user.is_authenticated:return render(request,'dashboard.html')
    else:return redirect('signin')

def signup(request):
    if request.user.is_authenticated:return render(request,'index.html')
    elif request.method=="POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists():messages.info(request, 'Username and Email already exists')
        elif User.objects.filter(username=username).exists():messages.info(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():messages.info(request, 'Email already exists')
        else:
            user = User.objects.create_user(username, email, password)
            db_users.insert_one({"username":username, "email":email, "password":password})
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect("dashboard")
        return redirect("signup")
    else:return render(request,'signup.html')

def signin(request):
    if request.user.is_authenticated:return redirect('dashboard')
    elif request.method == 'POST':    
        username = request.POST["username"]
        password = request.POST["password"]
        if '@' in username:username = User.objects.get(email=username.lower()).username
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        else:messages.info(request, 'User not found')
        return redirect("signin")
    else:return render(request,'signin.html')

def signout(request):
    if request.user.is_authenticated:logout(request)
    return redirect('signin')