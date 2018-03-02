from django.contrib import admin
from .models import Data, Dataset, Measurement, EnrichmentOutput

# Register your models here.

admin.site.register(Data)
admin.site.register(EnrichmentOutput)
admin.site.register(Dataset)
admin.site.register(Measurement)
