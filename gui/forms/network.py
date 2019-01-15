import django.forms.widgets as widg
from django import forms


class ListOfSpeciesFrom(forms.Form):
    list_of_species = forms.CharField(widget=widg.Textarea(), empty_value='')

    class Meta:
        fields = ('species_list',)


class NodeNeighborsForm(forms.Form):
    node = forms.CharField(widget=widg.TextInput({'class': 'form-group'}))
    up_stream = forms.BooleanField(
        widget=widg.CheckboxInput(attrs={'class': 'form-group'}),
        required=False)
    down_stream = forms.BooleanField(
        widget=widg.CheckboxInput(attrs={'class': 'form-group'}),
        required=False)
    max_dist = forms.ChoiceField(choices=((1, 1), (2, 2), (3, 3)), initial=1)

    class Meta:
        fields = ('node', 'up_stream', 'down_stream', 'max_dist')


class PathBetweenForm(forms.Form):
    start = forms.CharField(widget=widg.TextInput({'class': 'form-control'}))
    end = forms.CharField(widget=widg.TextInput({'class': 'form-control'}))
    bi_dir = forms.BooleanField(
        widget=widg.CheckboxInput(attrs={'class': 'form-control'}),
        required=False)

    class Meta:
        fields = ('start', 'end', 'bi_dir')
