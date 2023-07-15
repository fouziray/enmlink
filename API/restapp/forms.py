from django import forms
from .models import Profile

class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Profile
        fields = ['avatar']