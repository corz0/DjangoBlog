from django import forms

class ContactForm(forms.Form):
    full_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    content = forms.CharField(widget=forms.Textarea)

    def clean_email(self, *args, **kwargs):
        email=self.cleaned_data.get('email')
        print(email)
        if email.endswith(".edu"):
            raise forms.ValidationError('no es un dominio de correo valido')
        return(email)