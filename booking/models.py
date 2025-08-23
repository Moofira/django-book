from django.db import models
from django.contrib.auth.models import User  # <-- import User
from django.utils import timezone
from datetime import timedelta


class Seat(models.Model):
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)
    reserved_by = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True)
    reserved_until = models.DateTimeField(null=True, blank=True)

 
    def reserve(self, user, minutes=5):
        """Reserve seat temporarily"""
        self.is_reserved = True
        self.reserved_by = user
        self.reserved_until = timezone.now() + timedelta(minutes=minutes)
        self.save()

    def release(self):
        """Release seat back"""
        self.is_reserved = False
        self.reserved_by = None
        self.reserved_until = None
        self.save()

    def is_expired(self):
        """Check if reservation expired"""
        return self.is_reserved and self.reserved_until and timezone.now() > self.reserved_until

   
        

 



