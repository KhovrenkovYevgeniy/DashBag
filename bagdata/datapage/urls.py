from django.urls import path

from .views import *

urlpatterns = [
    path('home/', MainPage.as_view(), name='home'),
    path('pur/', PurchasesView.as_view(), name='purchases'),
    path('sal/', SalesView.as_view(), name='sales'),
    path('reg/', RegisterUser.as_view(), name='register'),
    path('', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]