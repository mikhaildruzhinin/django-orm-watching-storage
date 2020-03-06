from django.db import models
from django.utils import timezone

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
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )

    def get_duration(self):
        now = timezone.now()
        if not self.leaved_at:
            duration = now - self.entered_at
        else:
            duration = self.leaved_at - self.entered_at
        return duration

    def format_duration(self):
        duration = self.get_duration()
        seconds = int(duration.total_seconds())
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int((seconds % 3600) % 60)
        if hours == 0:
            hours = '00'
        elif hours < 10:
            hours = f'0{hours}'
        if minutes == 0:
            minutes = '00'
        elif minutes < 10:
            minutes = f'0{minutes}'
        if seconds == 0:
            seconds = '00'
        elif seconds < 10:
            seconds = f'0{seconds}'
        formatted_duration = f'{hours}:{minutes}:{seconds}'
        return formatted_duration

    def is_long(self):
        duration_minutes = int(self.get_duration().total_seconds() // 60)
        if duration_minutes > 60:
            return True
        return False