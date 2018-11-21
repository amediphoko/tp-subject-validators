from django.conf import settings

if settings.APP_NAME == 'tp_subject_validators':
    from .tests import models