from django import forms
from .models import Data
import django.forms.widgets as widg


class ProjectForm(forms.ModelForm):
    file = forms.FileField(label='')

    class Meta:
        model = Data
        fields = ('project_name',)


class ListOfSpeciesFrom(forms.Form):
    list_of_species = forms.CharField(widget=widg.Textarea())

    class Meta:
        fields = ('species_list',)


class NodeNeighborsForm(forms.Form):
    node = forms.CharField(widget=widg.TextInput({'class':'form-group'}))
    up_stream = forms.BooleanField(widget=widg.CheckboxInput(attrs={'class':'form-group'}), required=False)
    down_stream = forms.BooleanField(widget=widg.CheckboxInput(attrs={'class':'form-group'}), required=False)

    class Meta:
        fields = ('node', 'up_stream', 'down_stream')


class PathBetweenForm(forms.Form):
    start = forms.CharField(widget=widg.TextInput({'class':'form-control'}))
    end = forms.CharField(widget=widg.TextInput({'class':'form-control'}))
    bi_dir = forms.BooleanField(widget=widg.CheckboxInput(attrs={'class':'form-control'}), required=False)

    class Meta:
        fields = ('start', 'end', 'bi_dir')
