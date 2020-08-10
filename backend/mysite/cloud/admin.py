from django.contrib import admin
from .models import *
from django_paranoid.admin import ParanoidAdmin
# Register your models here.
admin.site.register(File)

class MyModelAdmin(ParanoidAdmin):
    pass