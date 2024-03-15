from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.db import IntegrityError
# Create your views here.


def user_register(request):
    if request.method=='POST':
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        pic=request.FILES.get('pic')
        try:
            validate_password(password1)
        except ValidationError as error:
            messages.error(request, '\n'.join(error.messages))
            return redirect('users:user_register')
        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.error(request,'Email already exists')
                return redirect('users:user_register')
            else:
                user=User.objects.create_user(email=email,first_name=first_name,last_name=last_name,password=password1)
                user.save()
                send_mail(
                    "Welcome Email",
                    "We are glad to see you in our ecom family",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request,'User created successfully')
                return redirect('users:user_login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('users:user_register')        
        
    return render(request, 'register.html')




def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            send_mail(
                    "Login Email",
                    "We are glad to see you back",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
            messages.success(request, 'Login successful')
            return redirect('shop:index')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('users:user_login')

    return render(request, 'login.html')



def user_logout(request):
    logout(request)

    messages.success(request, 'Logout successful')
    return redirect('shop:index')

@login_required(login_url='users:user_login')
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required(login_url='users:user_login')
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        send_mail(
                    "Update Profile",
                    "We are glad to inform that your profile has been updated",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
        messages.success(request, 'Profile updated successfully')
        return redirect('users:profile')

    return render(request, 'update_profile.html')

@login_required(login_url='users:user_login')
def delete_user(request):
    user = request.user
    send_mail(
                    "Delete User",
                    "Sorry to see you going",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
    user.delete()
    messages.success(request, 'User deleted successfully')
    return redirect('shop:index')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not User.objects.filter(email=email).exists():
            messages.info(request, 'User not found')
            return redirect('/forgot_password/')
        
        token = str(uuid.uuid4())
        user_obj = User.objects.get(email=email)
        
        try:
            forgot_obj = Forgot.objects.create(user=user_obj, forgot_password_token=token)
        except IntegrityError:
            forgot_obj = Forgot.objects.get(user=user_obj)
            forgot_obj.forgot_password_token = token
            forgot_obj.save()
        
        send_forgot_password_mail(email, token)
        messages.info(request, 'An email is sent')
        return redirect('/forgot_password/')
    
    return render(request, 'forgot_password.html')




def send_forgot_password_mail(email,token):
    subject='Change password Link'
    message= f"Click on link to change password http:127.0.0.1:8000/change_password/{token}/"
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def change_password(request,token):
    forgot_obj=Forgot.objects.filter(forgot_password_token=token).first()
    if request.method=='POST':
        new_password=request.POST.get('password1')
        confirm_password=request.POST.get('password2')
        user_id=request.POST.get('user_id')

        if user_id is None:
            messages.info(request,'User not found')
            return redirect(f'/change_password/{token}/')
        
        if new_password!=confirm_password:
            messages.info(request,'Password not same')
            return redirect(f'/change_password/{token}/')
        user_obj=User.objects.get(id=user_id)
        user_obj.set_password(new_password)
        user_obj.save()
        return redirect('users:user_login')
    
    context={'user_id':forgot_obj.user.id}
    return render(request,'change_password.html',context)