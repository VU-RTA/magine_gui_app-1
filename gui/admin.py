from django.contrib import admin
from .models import Data, Dataset, Measurement

# Register your models here.

admin.site.register(Data)
admin.site.register(Dataset)
admin.site.register(Measurement)
