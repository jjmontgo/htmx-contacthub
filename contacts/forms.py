from django import forms
from contacts.models import Contact
from django.core.exceptions import ValidationError

class ContactForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Contact Name'
        }),
    )

    email = forms.EmailField(
        widget = forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Email Address'
        }),
    )

    document = forms.FileField(
        widget = forms.FileInput(attrs={
            'class': 'file-input file-input-borderd w-full',
        }),
        required=False,
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        if name.startswith('X'):
            raise ValidationError('No names beginning with X!')
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Contact.objects.filter(
            user=self.initial.get('user'),
            email=email
        ).exists():
            raise ValidationError("Email already exists.")
        return email

    class Meta:
        model = Contact
        fields = ['name', 'email', 'document']
