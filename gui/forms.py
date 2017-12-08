from django import forms
import gui.models as models
import django.forms.widgets as widg


class ProjectForm(forms.ModelForm):
    file = forms.FileField(label='')

    class Meta:
        model = models.Data
        fields = ('project_name',)


class ListOfSpeciesFrom(forms.Form):
    list_of_species = forms.CharField(widget=widg.Textarea(), empty_value='')

    class Meta:
        fields = ('species_list',)


class ListOfSpeciesOntology(forms.Form):
    list_of_species = forms.CharField(widget=widg.Textarea(), empty_value='')
    CHOICES = (
        ('transcription_factors', 'transcription_factors'),
        ('pathways', 'pathways'),
        ('kinases', 'kinases'),
        ('drug', 'drug'),
        ('ontologies', 'ontologies')
    )
    ontology = forms.ChoiceField(choices=CHOICES)

    class Meta:
        fields = ('species_list', 'ontology')


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


class EnrichmentDatasetForm(forms.Form):
    project_name = forms.MultipleChoiceField(
        widget=widg.CheckboxSelectMultiple,
        choices=models.EnrichmentOutput.objects.all(

        ).values_list('project_name', 'project_name').distinct()
    )

    category = forms.MultipleChoiceField(
        widget=widg.CheckboxSelectMultiple,
        choices=models.EnrichmentOutput.objects.all(
        ).values_list('category', 'category').distinct()
    )

    dbs = forms.MultipleChoiceField(

        widget=widg.CheckboxSelectMultiple,
        choices=models.EnrichmentOutput.objects.all(

        ).values_list('db','db').distinct()
    )

    class Meta:
        fields = ['project_name', 'category', 'dbs', ]
