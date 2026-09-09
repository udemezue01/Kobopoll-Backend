from django.contrib import admin

from .models import Survey, Choice, Response

# Register your models here.

admin.site.register (Survey)

admin.site.register (Choice)

admin.site.register (Response)
