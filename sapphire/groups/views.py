from django.shortcuts import render, redirect
from django.http import HttpResponse

from groups.models import Group, Chat_Entry
from utility.models import Event
from groups.forms import NewGroupForm, NewChatEntryForm
from django.contrib.auth.models import User


# Create your views here.
def list(request):
    groups = Group.objects.order_by('hours')
    if request.user.is_authenticated():
        return render(request, 'groups/groupListView.html', {'groups': groups})
    else:
        return redirect('login')

def group(request, group_id):
    group = Group.objects.get(id=group_id)
    events = Event.objects.filter(parentGroup=group)
    is_owner = group.owner == request.user
    return render(request, 'groups/groupView.html', {'group':group, 'events':events, 'is_member':group.get_is_member(request.user), 'is_owner':is_owner})

def join(request, group_id):
    group = Group.objects.get(id=group_id)
    if (group.get_is_member(request.user) == False):
        group.volunteers.add(request.user)
        group.save()
    return redirect('/groups/'+str(group_id))

def changePermissionLevel(request, group_id, user_id):
    user = User.objects.get(id=user_id)
    group = Group.objects.get(id=group_id)
    if (request.user != group.owner):
        return HttpResponse('You don\'t have the right permissions to see this page.')

    for curr_user in group.volunteers.all():
        if (curr_user == user):
            group.volunteers.remove(user)
            group.organizers.add(user)
            group.save()
            return redirect('/groups/'+str(group_id))


    for curr_user in group.organizers.all():
        if (curr_user == user):
            group.organizers.remove(user)
            group.volunteers.add(user)
            group.save()
            return redirect('/groups/'+str(group_id))

    return redirect('/groups/'+str(group_id))



def add(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            form = NewGroupForm(owner=request.user)
        else:
            form = NewGroupForm(request.POST, owner=request.user)
            if form.is_valid():
                group = form.save(commit=False)
                group.save()

                return redirect("/groups/"+str(group.id))

        return render(request, 'groups/addGroup.html', {'form':form})

    else:
        return redirect('login')

def chat(request, group_id):
    group = Group.objects.get(id=group_id)

    if not Group.get_is_member(group, request.user):
        return HttpResponse('You don\'t have the right permissions to see this page. You must be a member to access this page.')

    chat_entries = Chat_Entry.objects.filter(parentGroup=group).order_by('datetime')
    if(request.method == 'POST'):
        form = NewChatEntryForm(request.POST, user=request.user, parentGroup=group)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.save()

            return redirect('/groups/'+str(group_id)+'/chat/')

    else:
        form = NewChatEntryForm(user=request.user, parentGroup=group)

    # Filter this by single slot events in the future
    return render(request, 'groups/chat.html', {'entries':chat_entries, 'form':form})
