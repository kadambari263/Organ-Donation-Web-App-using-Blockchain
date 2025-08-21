from django.db import models
from django.contrib.auth.models import User

class HospitalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.hospital_name} ({self.user.username})"
