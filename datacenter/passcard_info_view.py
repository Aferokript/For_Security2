from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import get_duration, format_duration
from django.utils.timezone import localtime
from django.utils import timezone


def passcard_info_view(request, passcode):
    this_passcard_visits = [{}]
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)

    for visit in visits:
        leaved_at = visit.leaved_at
        if leaved_at == None:
            leaved_at = timezone.now()
        count  = localtime(visit.leaved_at) - localtime(visit.entered_at)
        duration = format_duration(count)
        this_passcard_visits.append({'entered_at': visit.entered_at, 'duration': duration, 'is_strange': False})

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }

    return render(request, 'passcard_info.html', context)
