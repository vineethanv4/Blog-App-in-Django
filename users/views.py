from django.forms import forms
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)  # creates the instance of the UserRegisterForm which is written in forms.py file
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') # gives the username of the valid data in the written form.
            messages.success(request, f'Account created for {username}!')  # gives the message that account is created.
            return redirect('login') # redirects to the login page creating the account.
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html', {'form' : form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid() :
            u_form.save()
            p_form.save()
            messages.success(request,f'Your accounr has been Updated')
            return redirect('profile')


    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)



    context = {
        'u_form': u_form,
        'p_form': p_form

    }
    return render(request,'users/profile.html',context)
