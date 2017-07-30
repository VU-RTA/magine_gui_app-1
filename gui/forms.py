from django import forms

from .models import Data


class ProjectForm(forms.ModelForm):
    file = forms.FileField(label='')
    class Meta:
        model = Data
        fields = ('project_name',)
