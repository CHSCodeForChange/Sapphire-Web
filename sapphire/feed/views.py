from django.shortcuts import render, redirect
from django.http import HttpResponse

from feed.models import Feed_Entry
# Create your views here.
def feed(request):
    if request.user.is_authenticated():
        return render(request, "feed/feed.html")
    else:
        return redirect('login')
