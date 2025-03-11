
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import UserChangeForm , UserCreationForm
from .models import User, OtpCode


# Register your models here.

@admin.register(OtpCode)
class SmsCodeAdmin(admin.ModelAdmin):
    list_display = ('id','phone_number','code','created_at')



class ExtendUserAdmin(UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id','email','phone_number','is_superuser',)
    list_filter = ('is_superuser',)


    fieldsets = (
        (None, {'fields': ('email', 'full_name', 'phone_number','password')}),
        ('Permissions',{'fields':('is_active','last_login','is_superuser','is_staff','groups','user_permissions')})

    )

    add_fieldsets = ((None, {'fields': ('email', 'full_name', 'phone_number', 'password1','password2',)}),)

    readonly_fields = ('last_login',)
    search_fields = ('email', 'full_name', 'phone_number', )
    ordering = ('full_name',)
    filter_horizontal = ('groups','user_permissions',)


    def get_form(self, request, obj=None, **kwargs):
        the_from = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            the_from.base_fields['is_superuser'].disabled = True
        return the_from


admin.site.register(User,ExtendUserAdmin)



