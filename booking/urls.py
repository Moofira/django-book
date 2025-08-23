from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout_page, name="checkout"),
    path("create-checkout-session/", views.create_checkout_session, name="create_checkout_session"),
    path("success/", views.payment_success, name="success"),
    path("cancel/", views.payment_cancel, name="cancel"),
]