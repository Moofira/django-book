import stripe
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Seat
from .utils import release_expired_seats

@login_required
def select_seats(request):
    # Always free expired reservations before showing seats
    release_expired_seats()

    if request.method == "POST":
        selected_seats = request.POST.getlist("seats")  # seats selected
        for seat_id in selected_seats:
            seat = Seat.objects.get(id=seat_id)
            if not seat.is_reserved or seat.is_expired():
                seat.reserve(request.user, minutes=5)  # reserve for 5 min
        return redirect("payment_page")  # redirect to payment

    seats = Seat.objects.all()
    return render(request, "select_seats.html", {"seats": seats})


@login_required
def payment_success(request):
    # When payment is done, confirm or release seats
    seats = Seat.objects.filter(reserved_by=request.user, is_reserved=True)
    for seat in seats:
        if not seat.is_expired():
            # Payment done -> lock permanently
            seat.reserved_until = None
            seat.is_reserved = True
            seat.save()
        else:
            # Expired before payment
            seat.release()

    return render(request, "payment_success.html")

# Set your Stripe secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout_page(request):
    return render(request, "booking/checkout.html", {
        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY
    })

@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": "Movie Ticket",
                            },
                            "unit_amount": 500,
                        },
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url='http://127.0.0.1:8000/success/',
                cancel_url='http://127.0.0.1:8000/cancel/',
            )
            return redirect(session.url, code=303)
    else:
            return JsonResponse({"error": "Invalid request method."}, status=400)

def payment_cancel(request):
    return render(request, "booking/cancel.html")

