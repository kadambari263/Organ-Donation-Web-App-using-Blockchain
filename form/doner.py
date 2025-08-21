from django import forms
from home.model import Donor  # make sure 'models' not 'model'

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = '__all__'
