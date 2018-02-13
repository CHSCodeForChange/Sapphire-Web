from django.shortcuts import render, redirect
from django.http import HttpResponse


def home(request):
    return redirect('overview')

def overview(request):
    return render(request, "info/overview.html")

def codeforchange(request):
    return render(request, "info/codeforchange.html")

def pricing(request):
    return render(request, "info/pricing.html")
