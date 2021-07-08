from django.contrib import admin
from .models import OTP
# Register your models here.


class OTPAdmin(admin.ModelAdmin):
    list_display = ['id', 'value', 'user_id', 'valid_upto']


admin.site.register(OTP, OTPAdmin)

