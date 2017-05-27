# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

def home(request):
    numbers = {1,2,3,4,5}
    name = "Kristel Rosales"

    args = {'myName': name, 'numbers': numbers}
    return render(request,'accounts/home.html',args)
