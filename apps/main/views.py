from django.shortcuts import render
from apps.gnss.models import Mission, Receiver, SatelliteSystem


def mainPage(request):
    context = {
        'name': 'Baran',
        'mission_count': Mission.objects.count(),
        'receiver_count': Receiver.objects.count(),
        'satellite_count': SatelliteSystem.objects.count(),
    }
    return render(request, 'main/firstPage.html', context)


def projectIntroduction(request):
    context = {
        'name': 'introduce'
    }
    return render(request, 'main/projectIntroduction.html', context)
