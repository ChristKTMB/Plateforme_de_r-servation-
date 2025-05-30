from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_reservation_confirmation(reservation):
    """Envoie un email de confirmation pour une réservation"""
    context = {
        'reservation': reservation
    }
    
    # Render HTML content
    html_content = render_to_string(
        'bookings/emails/reservation_confirmation.html',
        context
    )
    
    # Create plain text version by stripping HTML
    text_content = strip_tags(html_content)
    
    # Create email
    subject = f"Confirmation de votre réservation - {reservation.event.title}"
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[reservation.user.email]
    )
    
    # Attach HTML version
    email.attach_alternative(html_content, "text/html")
    
    # Send email
    try:
        email.send()
        return True
    except Exception as e:
        # Log the error here if needed
        return False