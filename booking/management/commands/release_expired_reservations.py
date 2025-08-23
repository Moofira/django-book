from django.core.management.base import BaseCommand
from booking.models import Seat
from django.utils import timezone

class Command(BaseCommand):
    help = "Release expired seat reservations"

    def handle(self, *args, **kwargs):
        expired_seats = Seat.objects.filter(reserved_until__lt=timezone.now(), is_booked=False)
        count = expired_seats.count()

        for seat in expired_seats:
            seat.release()

        self.stdout.write(self.style.SUCCESS(f"Released {count} expired reservations"))
