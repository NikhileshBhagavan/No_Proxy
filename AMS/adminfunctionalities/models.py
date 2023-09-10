

# Create your models here.
from django.db import models
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.db.models.deletion import SET_NULL
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random
from django.http.response import HttpResponse
from home.models import *
from django.shortcuts import render,redirect



    