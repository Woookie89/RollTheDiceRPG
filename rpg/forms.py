from django import forms

from .models import Campaign, Character, Roll, Ruleset


CONTROL_CLASS = 'control'


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ('name', 'ruleset', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'Nazwa kampanii'}),
            'ruleset': forms.Select(attrs={'class': CONTROL_CLASS}),
            'description': forms.Textarea(attrs={'class': CONTROL_CLASS, 'rows': 4}),
        }


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ('name', 'ruleset', 'campaign', 'notes')
        widgets = {
            'name': forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'Imie postaci'}),
            'ruleset': forms.Select(attrs={'class': CONTROL_CLASS}),
            'campaign': forms.Select(attrs={'class': CONTROL_CLASS}),
            'notes': forms.Textarea(attrs={'class': CONTROL_CLASS, 'rows': 4}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['campaign'].queryset = Campaign.objects.filter(owner=user)
        self.fields['campaign'].required = False


class RollForm(forms.Form):
    label = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'np. Test Zrecznosci'}),
    )
    expression = forms.CharField(
        initial='1d20',
        widget=forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'np. 1d20+3 albo 2d6'}),
    )
    ruleset = forms.ModelChoiceField(
        queryset=Ruleset.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': CONTROL_CLASS}),
    )
    character = forms.ModelChoiceField(
        queryset=Character.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': CONTROL_CLASS}),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['character'].queryset = Character.objects.filter(owner=user, is_active=True)
