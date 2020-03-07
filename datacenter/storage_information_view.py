from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render

def storage_information_view(request):

    non_closed_visits = []
    active_visits = Visit.objects.filter(leaved_at=None)
    for visit in active_visits:
        visit_info = {
            'who_entered' : visit.passcard.owner_name,
            'entered_at' : visit.entered_at,
            'duration' : visit.format_duration(),
        }
        non_closed_visits.append(visit_info)

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
