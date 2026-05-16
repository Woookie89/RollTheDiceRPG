from django import forms

from .models import Campaign, Character, JournalEntry, Ruleset
from .services.character_presets import build_character_data, flatten_character_data


CONTROL_CLASS = 'control'


def apply_control_class(fields):
    for field in fields.values():
        classes = field.widget.attrs.get('class', '')
        if CONTROL_CLASS not in classes.split():
            field.widget.attrs['class'] = f'{classes} {CONTROL_CLASS}'.strip()


class CampaignForm(forms.ModelForm):
    name = forms.CharField(label='Nazwa kampanii')
    ruleset = forms.ModelChoiceField(label='System', queryset=Ruleset.objects.filter(is_active=True))
    description = forms.CharField(label='Opis', required=False)

    class Meta:
        model = Campaign
        fields = ('name', 'ruleset', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'Nazwa kampanii'}),
            'ruleset': forms.Select(attrs={'class': CONTROL_CLASS}),
            'description': forms.Textarea(attrs={'class': CONTROL_CLASS, 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_control_class(self.fields)


class CharacterForm(forms.ModelForm):
    name = forms.CharField(label='Imię postaci')
    ruleset = forms.ModelChoiceField(label='System', queryset=Ruleset.objects.filter(is_active=True))
    campaign = forms.ModelChoiceField(label='Kampania', queryset=Campaign.objects.none(), required=False)
    role = forms.CharField(label='Klasa / profesja / archetyp', required=False)
    origin = forms.CharField(label='Pochodzenie / motywacja', required=False)
    level = forms.CharField(label='Poziom / ważny zasób', required=False)
    resource = forms.CharField(label='Zasób systemowy', required=False)
    health = forms.CharField(label='Zdrowie / rany', required=False)
    notes = forms.CharField(label='Notatki', required=False)

    class Meta:
        model = Character
        fields = ('name', 'ruleset', 'campaign', 'role', 'origin', 'level', 'resource', 'health', 'notes')
        widgets = {
            'name': forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'Imię postaci'}),
            'ruleset': forms.Select(attrs={'class': CONTROL_CLASS}),
            'campaign': forms.Select(attrs={'class': CONTROL_CLASS}),
            'role': forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'np. wojownik, badaczka, wampirzy klan'}),
            'origin': forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'np. pochodzenie, motywacja, sekret'}),
            'level': forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'np. poziom, szczęście, człowieczeństwo'}),
            'resource': forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'np. KP, poczytalność, głód'}),
            'health': forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'np. PW, rany, stan zdrowia'}),
            'notes': forms.Textarea(attrs={'class': CONTROL_CLASS, 'rows': 4, 'placeholder': 'Krótki opis, cele i ważne szczegóły postaci'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['campaign'].queryset = Campaign.objects.filter(owner=user)
        self.fields['campaign'].required = False
        self.fields['campaign'].empty_label = 'Bez kampanii'
        self.fields['ruleset'].empty_label = None
        if self.instance and self.instance.pk:
            self.fields['campaign'].queryset = Campaign.objects.filter(owner=self.instance.owner)
            for key, value in flatten_character_data(self.instance.data).items():
                self.fields[key].initial = value
        apply_control_class(self.fields)

    def save(self, commit=True):
        character = super().save(commit=False)
        if character.campaign_id:
            character.ruleset = character.campaign.ruleset
        character.data = build_character_data(character.ruleset_id, self.cleaned_data)
        if commit:
            character.save()
            self.save_m2m()
        return character


class RollForm(forms.Form):
    label = forms.CharField(
        label='Etykieta',
        required=False,
        widget=forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'np. Test Zręczności'}),
    )
    context = forms.CharField(
        label='Kontekst',
        required=False,
        widget=forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'np. atak mieczem, śledztwo, presja czasu'}),
    )
    expression = forms.CharField(
        label='Rzut',
        initial='1d20',
        widget=forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'np. 1d20+3 albo 2d6'}),
    )
    ruleset = forms.ModelChoiceField(
        label='System',
        queryset=Ruleset.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': CONTROL_CLASS}),
    )
    character = forms.ModelChoiceField(
        label='Postać',
        queryset=Character.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': CONTROL_CLASS}),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['character'].queryset = Character.objects.filter(owner=user, is_active=True)
        self.fields['character'].empty_label = 'Bez postaci'
        apply_control_class(self.fields)


class JournalEntryForm(forms.ModelForm):
    title = forms.CharField(label='Tytuł')
    entry_type = forms.ChoiceField(label='Typ wpisu', choices=JournalEntry.TYPE_CHOICES)
    campaign = forms.ModelChoiceField(label='Kampania', queryset=Campaign.objects.none(), required=False)
    character = forms.ModelChoiceField(label='Postać', queryset=Character.objects.none(), required=False)
    body = forms.CharField(label='Treść')

    class Meta:
        model = JournalEntry
        fields = ('title', 'entry_type', 'campaign', 'character', 'body')
        widgets = {
            'title': forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'np. Trop w starej kamienicy'}),
            'entry_type': forms.Select(attrs={'class': CONTROL_CLASS}),
            'campaign': forms.Select(attrs={'class': CONTROL_CLASS}),
            'character': forms.Select(attrs={'class': CONTROL_CLASS}),
            'body': forms.Textarea(attrs={'class': CONTROL_CLASS, 'rows': 4, 'placeholder': 'Co warto zapamiętać przed następną sesją?'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['campaign'].queryset = Campaign.objects.filter(owner=user)
            self.fields['character'].queryset = Character.objects.filter(owner=user, is_active=True)
        self.fields['campaign'].empty_label = 'Bez kampanii'
        self.fields['character'].empty_label = 'Bez postaci'
        apply_control_class(self.fields)
