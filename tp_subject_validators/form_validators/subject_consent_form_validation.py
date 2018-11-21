from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from edc_form_validators import FormValidator


class SubjectConsentFormValidator(FormValidator):
    participant_screening_model = 'tp_screening.participantscreening'

    @property
    def participant_screening_model_cls(self):
        return django_apps.get_model(self.participant_screening_model)

    def clean(self):
        try:
            participant_screening = self.participant_screening_model_cls.objects.get(
                screening_identifier=self.cleaned_data.get('screening_identifier'))
        except ObjectDoesNotExist:
            raise ValidationError("Participant Screening Form not completed.",
                                  code="missing_subject_screening")

        self.validate_dob(cleaned_data=self.cleaned_data,
                          model_obj=participant_screening)
        self.validate_literacy(
            cleaned_data=self.cleaned_data, model_obj=participant_screening)
        self.validate_consent_datetime(cleaned_data=self.cleaned_data)

    def validate_dob(self, cleaned_data=None, model_obj=None):
        screening_age_in_years = relativedelta(
            model_obj.report_datetime.date(), cleaned_data.get('dob')).years
        if screening_age_in_years != model_obj.age_in_years:
            message = {'dob':
                       'Age mismatch. The date of birth entered does not match the age at '
                       f'screening. Expected {model_obj.age_in_years}. '
                       f'Got {screening_age_in_years}.'}
            self._errors.update(message)
            raise ValidationError(message)

    def validate_literacy(self, cleaned_data=None, model_obj=None):
        self.literate = cleaned_data.get('is_literate')
        if self.literate != model_obj.literacy:
            message = {'is_literate':
                       'The literate field does not match the literacy at the screening. '
                       f'Expected {model_obj.literacy}. Got {self.literate}.'}
            self._errors.update(message)
            raise ValidationError(message)

    def validate_consent_datetime(self, cleaned_data=None):
        condition = self.add_form and not cleaned_data.get('consent_datetime')
        self.required_if_true(
            condition=condition,
            field_required='consent_datetime',
            required_msg='Please provide the consent_datetime.',
            inverse=False
        )
