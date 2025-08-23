# utils.py
from .models import Seat
from django.utils import timezone

def release_expired_seats():
    expired_seats = Seat.objects.filter(is_reserved=True, reserved_until__lt=timezone.now())
    for seat in expired_seats:
        seat.release()