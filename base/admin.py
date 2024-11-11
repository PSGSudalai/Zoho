from django.contrib import admin
from .models import Lead,Status,Assign

admin.site.register(Status)
admin.site.register(Lead)
admin.site.register(Assign)
