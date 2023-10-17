from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="index"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('addschedule',views.addschedule,name="addschedule"),
    path('viewschedule',views.viewschedule,name="viewschedule"),
    path('updateschedule',views.updateschedule,name="updateschedule"),
]
