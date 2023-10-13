from django import forms
from django.contrib.auth.models import User



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
    
class UserRegistationForm(forms.ModelForm):
    password = forms.CharField(label="Kalit so'z", widget=forms.PasswordInput)
    password_2 = forms.CharField(label="Kalit so'zni tasdiqlash", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        
    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Parol kiritishda xatolik iltimos qaytadan kiriting')
        return data['password2']