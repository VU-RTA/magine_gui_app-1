from import_export import resources
from .models import Data


class PersonResource(resources.ModelResource):
    class Meta:
        model = Data
