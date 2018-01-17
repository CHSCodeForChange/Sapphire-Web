from django.shortcuts import render, redirect
from Teaching.models import Animal

# Create your views here.
def animal(request):
    animals = Animal.objects.all()
    return render(request, 'teaching/animal.html', {'animal':animals})
