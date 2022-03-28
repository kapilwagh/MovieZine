import csv, io
import re
import sys
import urllib
from csv import reader
import os.path
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.contrib.auth import authenticate
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserRegisterForm, ContactForm
from django.core.mail import send_mail
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .utils import Util
import jwt
from django.views.generic import ListView
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.

def home(request):
    return render(request, 'users/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            user = User.objects.get(username=username)
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('login')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            email_body = 'Greetings, \n Hey '+user.username+', use the link below to verify your email. If you have not requested for an account verification, you can safely ignore this email. \n'+absurl+'\n\n Regards, \n MovieZine'
            data = {
                'to': email,
                'email_body': email_body,
                'email_subject': 'Verify your email'
            }
            Util.send_email(data)
            return redirect('active_email')
    else :
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

def verify_email_page(request):
    return render(request, 'users/active_email.html')


def verifyEmail(request):
    token = request.GET.get('token')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        user = User.objects.get(id=payload['user_id'])
        if not user.is_authenticated:
            user.is_authenticated = True
            user.save()
        messages.success(request, f'Your Account has been Authenticated! You can now Login {user.username}!')
        return redirect('login')

    except jwt.ExpiredSignatureError as expired:
        return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST, template_name='blah.html')

    except jwt.exceptions.DecodeError as invalid:
        return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

    except :
        return Response({'error': 'Error'}, status=status.HTTP_400_BAD_REQUEST)


def about(request):
    return render(request, 'users/about.html')

def contact(request):
    form = ContactForm()
    if request.method=='POST':
        form= ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data.get('full_name')
            email_id = form.cleaned_data.get('email_id')
            message = form.cleaned_data.get('message')
            message= full_name + " with the email, " + email_id + ", sent the following message:\n\n" + message
            send_mail('Contact Us', message, email_id, ['thebodyworkks@gmail.com'], fail_silently=False)
            messages.success(request, f'Your message has been sent succesfully.')
            return redirect('home')
    context={'form':form}    
    return render(request, 'users/contact.html', context)

@login_required
def profile(request):
    return render(request, 'users/profile.html')

def userUpload(request):
    return render(request, 'users/userUpload.html')

def terms(request):
    return render(request, 'users/faq.html')

def faq(request):
    return render(request, 'users/faq.html')

@login_required
def watchlist(request):
    return render(request, 'users/watchlist.html') 

@login_required
def comments(request):
    return render(request, 'users/comments.html')

@login_required
def rating(request):
    return render(request, 'users/rating.html')