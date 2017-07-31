from django import forms

from .models import Data


class ProjectForm(forms.ModelForm):
    file = forms.FileField(label='')
    class Meta:
        model = Data
        fields = ('project_name',)


class ListOfSpeciesFrom(forms.Form):
    list_of_species = forms.CharField()
    class Meta:
        fields = ('species_list',)
