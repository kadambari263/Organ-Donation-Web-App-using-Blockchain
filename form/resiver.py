from django import forms
from home.model.resiver import Receiver

class ReceiverForm(forms.ModelForm):
    class Meta:
        model = Receiver
        fields = ['name', 'age', 'blood_group', 'organ_needed', 'mobile_number', 'hospital', 'place','email', 'aadhaar', 'gender', 'hla_a', 'hla_b', 'hla_dr']

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if len(mobile_number) != 10:
            raise forms.ValidationError('Mobile number must be 10 digits long.')
        return mobile_number
