from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .utility import *
from .models import OTP
import uuid
from datetime import datetime, timedelta


def index(request):
    return render(request, "index.html")

def registerationPage(request):
    context = {}
    if request.method == 'POST':

        context['firstname'] = request.POST.get('firstname')
        context['lastname'] = request.POST.get('lastname')
        context['username'] = request.POST.get('email')
        context['email'] = request.POST.get('email')
        context['password1'] = request.POST.get('password1')
        context['password2'] = request.POST.get('password2')

        (status, msg) = isValidForm(context)

        user = User.objects.filter(username=context.get('username')).first()
        if status:
            if user is None:
                user = User.objects.create_user(context['username'], context['email'], context['password1'])
                user.first_name = context['firstname']
                user.last_name = context['lastname']
                user.is_active = False
                user.save()
                value = getOTPValue()
                otp = OTP(value=value, user_id=user)
                otp.save()
                if sendMessage(user, otp):
                    msg = "Successfully Send Email"
                    messages.info(request, msg)
                    return render(request, 'verification.html', {'email': user.email})
                else:
                    msg = "Error: Please Check Your Email"
                    messages.info(request, msg)
                    return redirect('register')

            else:
                msg = "Error: Email Already Exist. Please Login"
                messages.info(request, msg)
                return redirect('login')

        else:
            messages.info(request, msg)
            return render(request, 'register.html')

    return render(request, 'register.html')


def verification(request, *args, **kwargs):
    if request.method == "POST":
        email = request.POST.get('email')
        otp_value = request.POST.get('otp')
        otp = OTP.objects.filter(value=otp_value).first()
        if otp is not None and otp.user_id.email == email:
            user = User.objects.get(id=otp.user_id_id)
            if user is not None:
                user.is_active = True
                otp.value = None
                otp.save()
                user.save()
            else:
                msg = "Error: Something Goes Wrong!"
                messages.info(request, msg)
                return redirect('register')

            msg = "Successfully Create Account. Please login"
            messages.info(request, msg)
            return redirect('login')
        else:
            msg = "Error: OTP Not Valid!"
            messages.info(request, msg)
    return render(request, 'verification.html')


def loginPage(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        # import pdb;
        # pdb.set_trace()

        if user is not None:
            login(request, user)
            msg = "Login Successfully"
            messages.info(request, msg)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return render(request, 'index.html')

        else:
            msg = "Error: Email and Password not Valid"
            messages.info(request, msg)
            return redirect('login')

    return render(request, 'login.html', context)


@login_required()
def logoutPage(request):
    logout(request)
    msg = "Logout Successfully"
    messages.info(request, msg)
    return redirect('index')


def password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")

        user = User.objects.filter(username=email).first()

        if user is None:
            msg = "Error: Email is Not Valid"
            messages.info(request, msg)
        else:
            otp = OTP.objects.filter(user_id=user).first()
            otp_value = getOTPValue()
            if otp is None:
                otp = OTP(value=otp_value, user_id=user)

            otp.value = otp_value
            otp.valid_upto = datetime.now() + timedelta(minutes=30)
            otp.save()

            if sendMessage(user, otp):
                msg = "Successfully Send Email"
                messages.info(request, msg)

            return render(request, 'password_conf.html', {'email': user.email})

    return render(request, 'passwordReset.html')


def password_check(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        
        if otpValidation(email, otp):
            msg = "Enter New Password"
            messages.info(request, msg)
            return render(request, 'password_reset_form.html', {'email': email})
        
        else:
            msg = "Error: Validation Fail, Please Check Email"
            messages.info(request, msg)
    return redirect('password-reset')


def password_set_form(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        context['email'] = username

        if len(password1) < 8:
            msg = "Error: Password must be 8 digits"
            messages.info(request, msg)
            return render(request, 'password_reset_form.html', context)
        

        if password1 == password2 and len(password1) > 0:
            user = User.objects.get(username=username)
            user.set_password(password1)
            # import pdb
            # pdb.set_trace()
            user.is_active = True
            user.save()
            msg = "Password Updated Successfully"
            messages.info(request, msg)
            return redirect('login')

        else:
            msg = "Error: Password May Not Matched"
            messages.info(request, msg)

    return render(request, 'password_reset_form.html', context)
