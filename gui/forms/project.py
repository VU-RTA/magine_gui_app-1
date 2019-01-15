from django import forms

import gui.models as models


class ProjectForm(forms.ModelForm):
    file = forms.FileField(label='')

    class Meta:
        model = models.Data
        fields = ('project_name',)
