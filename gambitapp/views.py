from django.shortcuts import render

# Create your views here.

from gambitapp.models import gambitStats

def index(request):
    motesLost = gambitStats.objects.all().count()


    context = {
            'motesLost': motesLost
    }

    return render(request, 'index.html', context=context)

from django.views import generic

class SomeListView(generic.ListView):
    model = gambitStats
    context_object_name = 'my_guard_view'
    queryset = gambitStats.objects.filter(guardianId=2305843009269921200)
