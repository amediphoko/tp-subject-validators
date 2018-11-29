from edc_form_validators import FormValidator


class CommunityEngagementFormValidator(FormValidator):
    def clean(self):
        self.validate_other_specify(
            field='community_problems',
            other_specify_field='community_problems_other',
            required_msg='Please specify other for community problems. ')

        cleaned_data = self.cleaned_data
        condition = cleaned_data.get('community_problems') is not None
        self.applicable_if_true(
            condition,
            field_applicable='together_in_solving'
        )
