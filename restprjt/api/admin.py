from django.contrib import admin
from  .models import User, Doctor
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','password','is_doctor']

@admin.register(Doctor)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','user','hospital','department']