from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistationForm
from ovoza.custom_permissions import OnlyLoogedSuperUser

# Create your views here.

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data['username'],
                                password=data['password']
                                )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('home')) 
                else:
                    messages = 'Kira olmaysiz'
            else:
                messages = "Foyddalanuvchi nomi yoki maxfiy so'z xato"
            context = {
                'messages': messages
            }
            return render(request, 'registration/login.html', context)
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'registration/login.html', context)



def user_logout(request):
    logout(request)
    return redirect(reverse('home'))
    
    
    
def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data["password"]
            )
            new_user.save()
            context = {
                'new_user': new_user
            }
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegistationForm()
        context = {"user_form": user_form}
    return render(request, "account/register.html", context)
        
    