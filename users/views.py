from django.shortcuts import render
import csv, io
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
# Create your views here.

def home(request):
    return render(request, 'users/home.html')

def login(request):
    return render(request, 'users/login.html')

def register(request):
    return render(request, 'users/register.html')

def logout(request):
    return render(request, 'users/logout.html')

def about(request):
    return render(request, 'users/about.html')

def contact(request):
    return render(request, 'users/contact.html')

def profile(request):
    return render(request, 'users/profile.html')

def userUpload(request):
    return render(request, 'users/userUpload.html')

def watchlist(request):
    return render(request, 'users/watchlist.html') 