from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy

from .forms import AddProductForm, RegisterUserForm, LoginUserForm
from .models import *
import datetime
from django.views.generic import ListView, CreateView
from django.db.models import Sum

date = datetime.datetime.now()
menu = [{'title': "Головна сторінка", 'url_name': 'home'},
        {'title': "Закупки", 'url_name': 'purchases'},
        {'title': "Історія продаж", 'url_name': 'sales'},
        {'title': "Вихід", 'url_name': 'logout'},
]





from django.shortcuts import redirect
from django.views.generic import ListView
from .models import Product, Story

class MainPage(ListView):
    model = Product
    template_name = 'datapage/index.html'
    context_object_name = 'products'
    queryset = Product.objects.all().values('name', 'code', 'quantity', 'price', 'arrived_date', 'expiration_date')
    context_object_name = 'maindata'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Головна сторінка'
        context['date'] = date.strftime("%Y-%m-%d")
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        code = request.POST.get('code')
        quantity = int(request.POST.get('quantity'))
        price = int(request.POST.get('price'))

        try:
            product = Product.objects.get(name=name, code=code)
            product.quantity -= quantity
            product.save()
        except Product.DoesNotExist:
            pass

        history = Story.objects.create(name=name, code=code, quantity_of_sold=quantity, price=price)

        return redirect('home')





class PurchasesView(ListView):
    model = Product
    template_name = 'datapage/purchases.html'
    context_object_name = 'buydata'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = date.strftime("%Y-%m-%d")
        context['menu'] = menu
        context['title'] = 'Закупки'
        context['form'] = AddProductForm()
        return context

    def post(self, request, *args, **kwargs):
        form = AddProductForm(request.POST)
        if form.is_valid():
            try:
                Product.objects.create(**form.cleaned_data)
                return redirect('purchases')
            except:
                form.add_error(None, 'Помилка з додаванням ')
        # If the form is not valid or the product could not be created, render the template with the form and the buydata queryset
        return self.render_to_response(self.get_context_data(form=form))





class SalesView(ListView):
    model = Story
    template_name = 'datapage/sales.html'
    context_object_name = 'sales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = date.strftime("%Y-%m-%d")
        context['menu'] = menu
        context['title'] = 'Історія продаж'
        context['last_sold_date'] = Story.objects.latest('sold_date').sold_date
        context['average_check'] = self.calculate_average_price()  # Вызов метода calculate_average_price и добавление значения в контекст
        return context

    def calculate_average_price(self):
        latest_sale = Story.objects.latest('sold_date')
        total_price = Story.objects.filter(sold_date=latest_sale.sold_date).aggregate(Sum('price'))['price__sum']
        average_check = total_price / 2
        return average_check







class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'datapage/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Реєстрація'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')




class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'datapage/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизація'
        return context

    def get_success_url(self):
        return reverse_lazy('home')




def logout_user(request):
    logout(request)
    return redirect('login')


def pageNotFound(request, exeption):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
