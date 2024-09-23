from .utils import generate_random_password
from django.db import models
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage

class Realtor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    is_mvp = models.BooleanField(default=False)
    hire_date = models.DateTimeField(default=datetime.now, blank=True)

    def save(self, *args, **kwargs):
        if not self.user:  # Only create a new user if one doesn't exist
            password = generate_random_password()
            user = User.objects.create(
                username=self.email,
                email=self.email,
                password=make_password(password),
                is_staff=True,
                is_active=True
            )
            self.user = user  # Link the user to the realtor

            # Send an email with the login credentials
            email_body = f"""
            <html>
                <body>
                    <h2 style="color: #333;">Your Realtor Account</h2>
                    <p>Hello {self.name},</p>
                    <p>Your login credentials are:</p>
                    <p>
                        <strong>Email:</strong> {self.email}<br>
                        <strong>Password:</strong> {password}
                    </p>
                    <hr>
                    <p style="color: #888;">This is an automated message. Please do not reply.</p>
                </body>
            </html>
            """

            email = EmailMessage(
                'Your Realtor Account',
                email_body,
                
                [self.email],
            )
            email.content_subtype = 'html'  # This ensures the email is sent as HTML
            email.send(fail_silently=False)

        super(Realtor, self).save(*args, **kwargs)  # Save the Realtor instance

    def __str__(self):
        return self.name
