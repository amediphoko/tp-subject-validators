from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import OTHER
from ..form_validators import CommunityEngagementFormValidator


@tag('ce')
class TestCommunityEngagementForm(TestCase):

    def test_other_specify_missing_comm_problems(self):
        cleaned_data = {
            'community_problems': OTHER,
            'community_problems_other': None
        }
        form_validator = CommunityEngagementFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('community_problems_other', form_validator._errors)

    def test_other_specify_provided(self):
        cleaned_data = {
            'community_problems': OTHER,
            'community_problems_other': 'some other made up problem'
        }
        form_validator = CommunityEngagementFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_comm_problems_not_other_field_other_valid(self):
        cleaned_data = {
            'community_problems': 'some made up problem',
            'community_problems_other': None
        }
        form_validator = CommunityEngagementFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_comm_problems_not_other_field_other_invalid(self):
        cleaned_data = {
            'community_problems': 'some made up problem',
            'community_problems_other': 'some other made up problem'
        }
        form_validator = CommunityEngagementFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('community_problems_other', form_validator._errors)