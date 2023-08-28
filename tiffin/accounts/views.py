from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import tree
from django.views.generic import CreateView
from .form import CustomerSignUpForm, EmployeeSignUpForm, ContactForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer, User, Feedback

def index(request):
    return render(request, 'index.html')

class customer_register(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class employee_register(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = 'employee_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class contact(CreateView):
    model = Feedback
    form_class = ContactForm
    template_name = 'contact.html'
    
    def form_valid(self, form):
        user = form.save()
        return redirect('/')


def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(User.is_customer==True,username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/accounts/student_home')#customer
            else:
                messages.error(request,"Invalid cusername or password")
        else:
                messages.error(request,"Invalid cusername or password")
    return render(request, 'login1.html',
    context={'form':AuthenticationForm()})

def login_request1(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(User.is_employee==True, username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/accounts/staff_home')
            else:
                messages.error(request,"Invalid vusername or password")
            print(user.is_employee)
        else:
                messages.error(request,"Invalid vusername or password")
               
    return render(request, 'login.html',
    context={'form':AuthenticationForm()})


def logout_view(request):
    logout(request)
    return redirect('/')

def Testurl(request):
    return HttpResponse("Ok")