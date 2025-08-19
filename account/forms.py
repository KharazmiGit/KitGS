from django.contrib import admin
from django import forms
from .models import GamAccount
from django.utils.safestring import mark_safe


class GamAccountForm(forms.ModelForm):
    class Meta:
        model = GamAccount
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Read-only widget
            self.fields['gam_password'].widget = ReadOnlyPasswordWidget()
            self.fields['gam_password'].disabled = True
            self.fields['gam_password'].help_text = "Password is securely stored and cannot be changed."
        else:
            # Editable password input
            self.fields['gam_password'].widget = forms.PasswordInput(attrs={
                'style': 'width: 237px;',
                'class': 'vTextField'
            })

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not self.instance.pk:
            instance.set_password(self.cleaned_data['gam_password'])
        if commit:
            instance.save()
        return instance


class ReadOnlyPasswordWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        masked = '●●●●●●●●' if value else ''
        html = f'<input type="password" value="{masked}" readonly style="width:260px;" class="vTextField" />'
        return mark_safe(html)
