from django.contrib import admin

# Register your models here.

from gambitapp.models import *

admin.site.register(gambitStats)
admin.site.register(GuardianId)
admin.site.reguster(GuardianClass)
