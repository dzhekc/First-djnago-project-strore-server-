from django.contrib import admin

# Register your models here.

from user.models import User
from products.admin import BasketAdmin
from user.models import EmailVerification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BasketAdmin,)

admin.site.register(EmailVerification)