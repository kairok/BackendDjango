from django.contrib import admin

# Register your models here.
from .models import *




admin.site.register(Request)
admin.site.register(Client)
admin.site.register(Problem)
admin.site.register(Master)
admin.site.register(Prioritet)


admin.site.register(Spec)
admin.site.register(Status)
admin.site.register(Firma)
