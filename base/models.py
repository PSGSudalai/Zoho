from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Status(models.Model):
    identity = models.CharField(max_length=100)

    def __str__(self):
        return self.identity
    
class Assign(models.Model):
    assigned_to = models.CharField(max_length=100)
    
    def __str__(self):
        return self.assigned_to

    
class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15) 
    gender = models.CharField(max_length=100) 
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    passout = models.CharField(max_length=255)
    college_name = models.CharField(max_length=255)
    tech_field = models.CharField(max_length=255)
    source=models.CharField(max_length=255)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    is_lead = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)  
    follow_up = models.DateField(null=True, blank=True)
    assign_to = models.ForeignKey(Assign, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.name



