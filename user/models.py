from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_image',null=True,blank=True)
    is_verified_email = models.BooleanField(default=False)

class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"Emailverification object {self.user.email}"

    def send_ver_code(self):
        link = reverse('users:email_verify',args=(self.user.email,self.code))
        verify_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f"подтверждение учётной записи для {self.user.username}"
        message = f'Для подтверждения учётной записи для {self.user.email}, alterociver@gmail.com перейдите по ссылке {verify_link}'

        send_mail(
            subject = subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list = [self.user.email,'alterociver@gmail.com'],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False

# Create your models here.
