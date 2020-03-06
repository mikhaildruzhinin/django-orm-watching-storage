from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render

def storage_information_view(request):

    non_closed_visits = []
    active_visits = Visit.objects.filter(leaved_at=None)
    for visit in active_visits:
        d = {}
        d['who_entered'] = visit.passcard.owner_name
        d['entered_at'] = visit.entered_at
        d['duration'] = visit.format_duration()
        non_closed_visits.append(d)

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
