from django.contrib import admin
from . import models

admin.site.register(models.user)
admin.site.register(models.resident)
admin.site.register(models.doctor)
admin.site.register(models.Service_Team)
admin.site.register(models.family)
admin.site.register(models.message)
admin.site.register(models.appoint)