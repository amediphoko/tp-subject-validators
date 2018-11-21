from dateutil.relativedelta import relativedelta
from django.test.testcases import TestCase
from django.core.exceptions import ValidationError
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO
from .models import ParticipantScreening
from ..form_validators import SubjectConsentFormValidator


class TestSubjectConsentForm(TestCase):

    def setUp(self):
        self.screening_identifier = 'ABC1234'
        self.participantscreening = ParticipantScreening.objects.create(
            screening_identifier=self.screening_identifier, age_in_years=18,
            literacy=YES)
        screening_model = 'tp_subject_validators.participantscreening'
        SubjectConsentFormValidator.participant_screening_model = screening_model

    def test_subject_screening_valid(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=18)).date(),
            'is_literate': YES
        }
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_subject_screening_invalid(self):
        cleaned_data = {
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=18)).date()
        }
        form_validator = SubjectConsentFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('missing_subject_screening', form_validator._error_codes)

    def test_consent_datetime_required(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': None,
            'dob': (get_utcnow() - relativedelta(years=18)).date(),
            'is_literate': YES
        }
        form_validator = SubjectConsentFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('consent_datetime', form_validator._errors)

    def test_consent_datetime_provided(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=18)).date(),
            'is_literate': YES
        }
        form_validator = SubjectConsentFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_dob_mismatch_age_at_screening(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=20)).date(),
            'is_literate': YES
        }
        form_validator = SubjectConsentFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('dob', form_validator._errors)

    def test_dob_matches_age_at_screening(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=18)).date(),
            'is_literate': YES
        }
        form_validator = SubjectConsentFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_is_literate_mismatch_literacy_at_screening(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=18)).date(),
            'is_literate': NO
        }
        form_validator = SubjectConsentFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('is_literate', form_validator._errors)

    def test_is_literate_matches_literacy_at_screening(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=18)).date(),
            'is_literate': YES
        }
        form_validator = SubjectConsentFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
