from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from users.models import UserProfile, PremiumAccount

import paypalrestsdk


@login_required
def process_payment(request):
    """
    View to process the PayPal payment.
    """
    # Set up PayPal SDK configuration
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_SECRET,
    })

    # Create a payment object
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('payment_success')),
            "cancel_url": request.build_absolute_uri(reverse('payment_cancel')),
        },
        "transactions": [{
            "amount": {
                "total": "5.00",  # Actual payment amount
                "currency": "PLN"   # Actual currency code
            },
            "description": "Aktualizacja konta do Premium"  # Description of the payment
        }]
    })

    # Create the payment and get the approval URL
    if payment.create():
        approval_url = next(link.href for link in payment.links if link.rel == 'approval_url')
        return redirect(approval_url)
    else:
        # Failed to create payment, handle the error and display a message to the user
        messages.error(request, "Problem z przetwarzaniem płatności: " + payment.error['message'])
        return redirect('profile')


@login_required
def payment_success(request):
    """
    View to handle the success response from PayPal after payment.
    """
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Check if the user already has a premium account
    if user_profile.premium_account:
        premium_account = user_profile.premium_account
    else:
        # If the user does not have a premium account, create a new one
        premium_account = PremiumAccount(user=request.user)

    # Calculate the start and end date for the PremiumAccount
    start_date = timezone.now()
    end_date = start_date + timedelta(days=30)

    # Update the PremiumAccount with the new dates
    premium_account.start_date = start_date
    premium_account.end_date = end_date
    premium_account.save()

    # Update the UserProfile's premium_account field
    user_profile.premium_account = premium_account
    user_profile.save()

    messages.success(request, "Płatność przebiegła pomyślnie. Twoje konto jest teraz kontem Premium.")

    return redirect('profile')  # Redirect the user to the profile page or any other appropriate page

@login_required
def payment_cancel(request):
    """
    View to handle the cancellation of payment.
    """
    messages.warning(request, "Płatność została odrzucona. Twoje konto nie zostało podniesione do statusy Premium.")
    return redirect('profile')
