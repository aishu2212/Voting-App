from django import forms
from .models import Voter, Candidate, Constituency
from django.core.exceptions import ValidationError

class VoterRegistrationForm(forms.ModelForm):
    voter_id = forms.EmailField()
    full_name = forms.CharField(max_length=255)
    date_of_birth = forms.DateField()
    constituency = forms.ModelChoiceField(queryset=Constituency.objects.all())
    unique_voter_code = forms.CharField(max_length=8)
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Voter
        fields = ['voter_id', 'full_name', 'date_of_birth', 'constituency', 'unique_voter_code', 'username', 'password']

    def clean_unique_voter_code(self):
        submitted_uvc = self.cleaned_data['unique_voter_code']
        predefined_uvcs = [
            'HH64FWPE', 'BBMNS9ZJ', 'KYMK9PUH', 'WL3K3YPT', 'JA9WCMAS',
            'Z93G7PN9', 'WPC5GEHA', 'RXLNLTA6', '7XUFD78Y', 'DBP4GQBQ',
            'ZSRBTK9S', 'B7DMPWCQ', 'YADA47RL', '9GTZQNKB', 'KSM9NB5L',
            'BQCRWTSG', 'ML5NSKKG', 'D5BG6FDH', '2LJFM6PM', '38NWLPY3',
            '2TEHRTHJ', 'G994LD9T', 'Q452KVQE', '75NKUXAH', 'DHKVCU8T',
            'TH9A6HUB', '2E5BHT5R', '556JTA32', 'LUFKZAHW', 'DBAD57ZR',
            'K96JNSXY', 'PFXB8QXM', '8TEXF2HD', 'N6HBFD2X', 'K3EVS3NM',
            '5492AC6V', 'U5LGC65X', 'BKMKJN5S', 'JF2QD3UF', 'NW9ETHS7',
            'VFBH8W6W', '7983XU4M', '2GYDT5D3', 'LVTFN8G5', 'UNP4A5T7',
            'UMT3RLVS', 'TZZZCJV8', 'UVE5M7FR', 'W44QP7XJ', '9FCV9RMT',
        ]

        if submitted_uvc not in predefined_uvcs:
            raise ValidationError('Invalid/ Used Unique Voter Code')

        return submitted_uvc

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

class VoteForm(forms.Form):
    candidate = forms.ModelChoiceField(queryset=Candidate.objects.all(), empty_label=None)
    
class ElectionCommissionLoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)