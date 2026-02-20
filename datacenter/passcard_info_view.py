from django.utils.timezone import localtime
from django.utils import timezone


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []

    for visit in visits:
        minutes = get_duration(visit)
        fix_time = formated_duration(minutes)
        name = visit.passcard.owner_name
        entered_at = visit.entered_at
        non_closed_visit = {
            'who_entered': name,
            'entered_at': entered_at,
            'duration': fix_time
        }
        non_closed_visits.append(non_closed_visit)

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
