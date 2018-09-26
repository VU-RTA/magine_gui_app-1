from gui.models import Data
from data_format.format import process_raptr_zip


def add_project_from_zip(proj_name, filename):
    print('saving {}'.format(proj_name))
    Data.objects.filter(project_name=proj_name).delete()
    new = Data.objects.create(project_name=proj_name)
    print(filename)
    df = process_raptr_zip(filename)
    new.set_exp_data(df, set_time_point=True)
    new.save()
    print('saved')
