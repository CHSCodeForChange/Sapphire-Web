from django.shortcuts import render, redirect
from django.http import HttpResponse

from feed.models import Feed_Entry
# Create your views here.
def feed(request):
    if request.user.is_authenticated():
        feed_entries = Feed_Entry.objects.order_by('-datetime')
        return render(request, 'feed/feed.html', {'feed_entries':feed_entries})
    else:
        return redirect('login')
