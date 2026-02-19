from datacenter.models import Passcard, Visit
from django.shortcuts import render
import datetime
from django.utils import timezone
from .models import get_duration, format_duration


def storage_information_view(request):
    non_closed_visits = {}
    visits = Visit.objects.filter(leaved_at=None)
    for visit in visits:
        minutes = get_duration(visit)
        duration = format_duration(minutes)
        name = visit.passcard.owner_name
        entered_at = visit.entered_at
        non_closed_visits.append({'who_entered': name, 'entered_at': entered_at, 'duration': duration})

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
