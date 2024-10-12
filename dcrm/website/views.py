from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm 
from  django.contrib.auth.models import auth 
from  django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from . models import Record
from . models import Gamedata
from django.shortcuts import render, redirect
from .forms import CreateRecordForm,CreateUserForm,LoginForm
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib import messages
from django.conf import settings
import requests  
# Create your views here.
def home(request):
    return render(request, 'website/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully")
            return redirect('my-login')
    context = {"form": form}


    return render(request,'website/register.html',context=context) 

def my_login(request): 
    form =  LoginForm()   

    if  request.method=="POST" : 
            form = LoginForm(request, data=request.POST)   

            if form.is_valid(): 
               username = request.POST.get('username') 
               password = request.POST.get('password') 

               user = authenticate(request, username=username, password=password) 

               if user is not None :
                  auth.login(request, user)
                  messages.success(request,"Logged in") 
                  return redirect('dashboard')  

    context = {'login_forms':form}
    return render(request,'website/my-login.html', context = context)

def user_logout(request):
    auth.logout(request)
    messages.success(request,"Logged out")
    return redirect("my-login")

#dashboard

@login_required(login_url='my-login')
def dashboard(request):

    my_records = Record.objects.all()
    context = {'records': my_records}
    return render(request,'website/dashboard.html',context=context)

# record creation
@login_required(login_url='my_login')
def create_record(request):
    
    form = CreateRecordForm()
    if request.method == "POST":
        form = CreateRecordForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Your record was created!")
            return redirect("dashboard")

   
        
    context = {'create_form': form}
    return render(request, 'website/create-record.html',context=context)

# update a record
@login_required(login_url='my-login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)

    if request.method == "POST":
        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():
            form.save()
            messages.success(request, "Record was updated")
            return redirect("dashboard")
        
    context ={'update_form': form}
    return render(request, 'website/update-record.html',context=context)

#read a single record

@login_required(login_url='my-login')
def singular_record(request,pk):

    one_record = Record.objects.get(id=pk)
    context = {'record':one_record}
    return render(request,'website/view-record.html', context= context)


@login_required(login_url='my-login')
def delete_record(request,pk ):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, "The record was deleted")





    return redirect("dashboard")


def products(request):
    return render(request, 'website/products.html')

def game_date(request):
    
    data = Gamedata.objects.all()
    context = {'data': data}

    return render(request, 'website/game-data.html',context=context)
                  

def weather_data(request):
    print("loading weather view")
    if request.method == "POST":
        city=request.POST.get("city")
        key = settings.MY_API_KEY

        BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q="

        url = BASE_URL + city + "&appid=" + key

        json_data = requests.get(url).json()

        weather = json_data['weather'][0]['main']
        temperature = int(json_data['main'])
        min = int(json_data['main']['temp_min'] - 273.15)
        max = int(json_data['main']['temp_max'] - 273.15)
        icon = json_data['weather'][0]['icon']

        data = {
            "location":city,
            "weather": weather,
            "temperature": temperature,
            "min": min,
            "max": max,
            "icon" : icon
           
        }

        context = {'data': data}

        return render(request, 'website/weather-data.html', context=context)
    else:
        return render(request, 'website/weather-data.html')
    
        



































































     





    