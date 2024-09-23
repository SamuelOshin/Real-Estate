from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import BadHeaderError
import smtplib
from .models import Contact
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_password_reset_email(user_email, domain, uid, token):
    subject = 'Password Reset Request'
    from_email = 'your_email@example.com'
    to_email = [user_email]

    # Render the HTML template as a string
    html_content = render_to_string('registration/password_reset_email.html', {
        'domain': domain,
        'uid': uid,
        'token': token,
        'user_email': user_email,
    })

    # Create an email message object
    email = EmailMultiAlternatives(subject, '', from_email, to_email)
    email.attach_alternative(html_content, "text/html")  # Attach the HTML content
    email.send()  # Send the email

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        #  Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing')
                return redirect('/listings/'+listing_id)

        try:
            
            # Send email
            email_body = f"""
            <html>
                <body>
                    <h2 style="color: #333;">Property Listing Inquiry</h2>
                    <p>There has been an inquiry for <strong>{listing}</strong>.</p>
                    <p>
                        <strong>Name:</strong> {name}<br>
                        <strong>Email:</strong> {email}<br>
                        <strong>Phone:</strong> {phone}<br>
                        <strong>Message:</strong> {message}
                    </p>
                    <hr>
                    <p style="color: #888;">This is an automated message. Please do not reply.</p>
                </body>
            </html>
            """

            email = EmailMessage(
                'Property Listing Inquiry',
                email_body,
                
                [realtor_email, "samuelt.oshin@gmail.com"],
            )
            email.content_subtype = 'html'  # This is the key to sending an HTML email
            email.send(fail_silently=False)

            # Save contact only if email is sent successfully
            contact = Contact(
                listing=listing,
                listing_id=listing_id,
                name=name,
                email=email,
                phone=phone,
                message=message,
                user_id=user_id
            )
            contact.save()
            
            messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
        
        except BadHeaderError:
            messages.error(request, 'Invalid header found.')
            return redirect('/listings/'+listing_id)

        except smtplib.SMTPException as e:
            # Log the error or notify the admin
            print(f"SMTP error occurred: {e}")
            messages.error(request, 'There was an error sending your email. Please try again later.')
            return redirect('/listings/'+listing_id)

        except Exception as e:
            # Handle other possible exceptions
            print(f"An error occurred: {e}")
            messages.error(request, 'An unexpected error occurred. Please try again later.')
            return redirect('/listings/'+listing_id)

    return redirect('/listings/'+listing_id)


