from django import forms
from django.core.exceptions import ValidationError
from .models import Feedback


class ContactForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = [
            'name',
            'phone',
        ]
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'phone' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
        }

    # def clean_phone(self):
    #     phone = self.cleaned_data['phone']
    #
    #     if len(phone) < 10:
    #         raise ValidationError('Неверный номер телефона')
    #     return phone
