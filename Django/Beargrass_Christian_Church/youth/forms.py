from django import forms
from .models import ChurchGoer


class ChurchGoerForm(forms.ModelForm):
    class Meta:
        model = ChurchGoer
        fields = (
            'first_name', 'middle_name', 'maiden_name', 'nickname', 'birthday', 'name_of_guardian', 'home_church',
            'family_are_beargrass_members', 'address', 'email', 'school', 'degree', 'employer', 'gender',
            'facebook_URL', 'google_plus_URL', 'instagram_URL', 'snapchat_URL', 'twitter_URL', 'married',
            'name_of_spouse', 'name_of_child', 'surname')
