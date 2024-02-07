from django.urls import path
from . import views

urlpatterns = [
    path('process-payment/', views.process_payment, name='process_payment'),
    # URL pattern for processing the PayPal payment

    path('payment-success/', views.payment_success, name='payment_success'),
    # URL pattern for handling the success response from PayPal after payment

    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    # URL pattern for handling the cancellation of payment
]
