from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow


class ParticipantScreening(BaseUuidModel):

    screening_identifier = models.CharField(
        max_length=50,
        unique=True)

    report_datetime = models.DateTimeField(
        default=get_utcnow)

    age_in_years = models.IntegerField()

    literacy = models.CharField(max_length=3)
