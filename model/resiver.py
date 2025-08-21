from django.db import models
from home.model.doner import Donor

class Receiver(models.Model):
    matched_donor = models.ForeignKey(Donor, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    blood_group = models.CharField(max_length=3)
    organ_needed = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15)
    hospital = models.CharField(max_length=100, blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    status = models.CharField(max_length=50, default="waiting")  # Status can be "waiting", "approved", "rejected"
    # models.py
    match_score = models.FloatField(default=0.0)


    # Add the new fields
    aadhaar = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    hla_a = models.CharField(max_length=20, blank=True, null=True)
    hla_b = models.CharField(max_length=20, blank=True, null=True)
    hla_dr = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
