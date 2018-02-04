from django.shortcuts import render, redirect
from django.http import HttpResponse

from groups.models import Group
from utility.models import Event
from groups.forms import NewGroupForm


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
    return render(request, 'groups/groupView.html', {'group':group, 'events':events})

def join(request, group_id):
    group = Group.objects.get(id=group_id)
    group.volunteers.add(request.user)
    group.save()
    print("hello world")
    return redirect('/groups/'+str(group_id))

def changePermissionLevel(request, group_id, user):
    group = Group.objects.get(group_id)
    if (request.user != group.owner):
        return HttpResponse('You don\'t have the right permissions to see this page.')

    for curr_user in group.volunteers.all():
        if (curr_user == user):
            groups.volunteers.remove(user)
            groups.organizer.add(user)

    for curr_user in group.organizers.all():
        if (curr_user == user):
            groups.organizers.remove(user)
            groups.volunteers.add(user)

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
