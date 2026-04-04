from django.contrib import admin
from .models import EmberUser, Shelter, NGOProfile, History
# Register your models here.

admin.site.register(EmberUser)
admin.site.register(Shelter)
admin.site.register(NGOProfile)
admin.site.register(History)
