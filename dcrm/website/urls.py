from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name=""),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('user-logout', views.user_logout, name= "user-logout"),


    #read
    
    path('dashboard', views.dashboard, name="dashboard"),

    #create
    path('create-record', views.create_record,name="create-record"),

    #update
    path('update-record/<int:pk>', views.update_record, name="update-record"),

    #view a single record

    path('record/<int:pk>',views.singular_record,name="record"),

    # Delete a record

    path('delete-record/<int:pk>', views.delete_record, name="delete-record"),

    # product overview

    path('products', views.products, name = "products"),
    
    #data page

    path('game-data', views.game_date, name="game-data"),

    path('weather-data',views.weather_data, name="weather-data"),




]


