import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magine_gui_app.settings')
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path)

from django.core.wsgi import get_wsgi_application
get_wsgi_application()
from gui.models import Data


def add_cisplatin():

    Data.objects.all().delete()

    new = Data.objects.create(project_name='cisplatin_test')
    new.set_exp_data(
        os.path.join(os.path.dirname(__file__),
                     'norris_et_al_2017_cisplatin_data.csv.gz')
    )
    new.save()


if __name__ == '__main__':
    add_cisplatin()