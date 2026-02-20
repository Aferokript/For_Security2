from django.db import models
from django.utils.timezone import localtime
from django.utils import timezone
import datetime


SECONDS = 60

def get_duration(visit):
    if visit.leaved_at is None:
        end_time = timezone.now()
    else:
        end_time = visit.leaved_at

    counted_time = localtime(end_time) - localtime(visit.entered_at)
    return counted_time


def formated_duration(duration):
    total_minutes = duration.total_seconds() // SECONDS
    hours = int(total_minutes // SECONDS)
    minutes = int(total_minutes % SECONDS)
    return f'{hours}:{minutes:02d}'


def check_visit(visit, limit=60):
    inside_time = get_duration(visit)
    minutes = inside_time.total_seconds() // SECONDS
    return minutes <= limit

class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )
