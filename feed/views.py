from django.shortcuts import render, redirect
from django.http import HttpResponse

from feed.models import Feed_Entry
from groups.models import Group
# Create your views here.
def feed(request):
    if request.user.is_authenticated():
        groups = Group.get_is_member_list(request.user)
        feed_entries = None
        for group in groups:
            if (feed_entries==None):
                feed_entries=Feed_Entry.objects.filter(group=group).filter(private=False)
            elif (feed_entries==None and group.get_is_organzer):
                feed_entries=Feed_Entry.objects.filter(group=group)
            elif group.get_is_organzer:
                groups_entrys = Feed_Entry.objects.filter(group=group)
                feed_entries=feed_entries.union(groups_entrys)
            else:
                groups_entrys = Feed_Entry.objects.filter(group=group).filter(private=False)
                feed_entries=feed_entries.union(groups_entrys)

        if (not(feed_entries==None)):
            feed_entries = feed_entries.order_by('-datetime')
        return render(request, 'feed/feed.html', {'feed_entries': feed_entries, 'groups':groups})
    else:
        return redirect('login')


def filterByGroup(request, group_id):
    group = Group.objects.get(id=group_id)
    if (request.user.is_authenticated() and group.get_is_member(request.user)):
        groups = Group.get_is_member_list(request.user)
        feed_entries = Feed_Entry.objects.filter(group=group).order_by('-datetime') #feed entries are sorted from most recent to least recent
        return render(request, 'feed/feed.html', {'feed_entries':feed_entries, 'groups':groups})
    else:
        if (not(group.get_is_member(request.user))):
            return redirect('feed')
        else:
            return redirect('login')
