from django.contrib import admin
from django.urls import path
from . import views

app_name = "email"
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/resend-verification/<str:email>', views.resend_verification, name='resend_verification'),
]
