from celery import shared_task
from .utils import release_expired_seats

@shared_task
def cleanup_expired_reservations():
    release_expired_seats()