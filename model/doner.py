from django.db import models
from django.contrib.auth.models import User

class Donor(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ],blank=True,null=True)
    aadhaar = models.CharField(max_length=12,null=True,blank=True)
    blood_group = models.CharField(max_length=10)
    hla_a = models.CharField(max_length=20, blank=True)
    hla_b = models.CharField(max_length=20, blank=True)
    hla_dr = models.CharField(max_length=20, blank=True)
    organ = models.CharField(max_length=50)
    hospital = models.CharField(max_length=100,blank=True)
    place = models.CharField(max_length=100,blank=True)
    mobile_number = models.CharField(max_length=15,blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.organ})"
