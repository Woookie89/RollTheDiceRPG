from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CampaignForm, CharacterForm, JournalEntryForm, RollForm
from .models import Campaign, Character, JournalEntry, Roll, Ruleset
from .services.dice import DiceExpressionError, roll_expression


ROLL_PRESETS = {
    'dnd-test': ('Test d20', '1d20'),
    'dnd-attack': ('Atak d20', '1d20'),
    'percentile-test': ('Test d100', '1d100'),
    'year-zero-pool': ('Pula d6', '6d6'),
    'vampire-pool': ('Pula Wampira', '5d10'),
    'kult-test': ('Test Kult', '2d10'),
}


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    rulesets = Ruleset.objects.filter(is_active=True)[:6]
    return render(request, 'rpg/landing.html', {'rulesets': rulesets})


@login_required
def dashboard(request):
    characters = Character.objects.filter(owner=request.user).select_related('ruleset', 'campaign')
    active_character = characters.order_by('-updated_at').first()
    campaigns = Campaign.objects.filter(owner=request.user).select_related('ruleset').annotate(
        character_count=Count('characters')
    )
    recent_rolls = Roll.objects.filter(user=request.user).select_related('ruleset', 'character')[:8]
    journal_entries = JournalEntry.objects.filter(user=request.user).select_related('campaign', 'character')[:5]
    roll_form = RollForm(user=request.user)
    journal_form = JournalEntryForm(user=request.user)
    return render(
        request,
        'rpg/dashboard.html',
        {
            'characters': characters,
            'active_character': active_character,
            'campaigns': campaigns,
            'recent_rolls': recent_rolls,
            'journal_entries': journal_entries,
            'roll_form': roll_form,
            'journal_form': journal_form,
        },
    )


@login_required
def campaign_create(request):
    if not request.user.is_game_master:
        messages.warning(request, 'Tworzenie kampanii jest dostępne w roli Mistrza Gry.')
        return redirect('profile')
    form = CampaignForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        campaign = form.save(commit=False)
        campaign.owner = request.user
        campaign.save()
        campaign.members.create(user=request.user, role='game_master')
        return redirect('dashboard')
    return render(request, 'rpg/campaign_form.html', {'form': form})


@login_required
def campaign_edit(request, pk):
    if not request.user.is_game_master:
        messages.warning(request, 'Edycja kampanii jest dostępna w roli Mistrza Gry.')
        return redirect('campaign-detail', pk=pk)
    campaign = get_object_or_404(Campaign, pk=pk, owner=request.user)
    form = CampaignForm(request.POST or None, instance=campaign)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('campaign-detail', pk=campaign.pk)
    return render(request, 'rpg/campaign_form.html', {'form': form, 'campaign': campaign})


@login_required
def campaign_detail(request, pk):
    campaign = get_object_or_404(
        Campaign.objects.select_related('ruleset'),
        pk=pk,
        owner=request.user,
    )
    characters = campaign.characters.filter(owner=request.user).select_related('ruleset')
    rolls = campaign.rolls.filter(user=request.user).select_related('character')[:8]
    journal_entries = campaign.journal_entries.filter(user=request.user).select_related('character')[:8]
    return render(
        request,
        'rpg/campaign_detail.html',
        {
            'campaign': campaign,
            'characters': characters,
            'rolls': rolls,
            'journal_entries': journal_entries,
        },
    )


@login_required
def character_create(request):
    form = CharacterForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        character = form.save(commit=False)
        character.owner = request.user
        if character.campaign_id:
            character.ruleset = character.campaign.ruleset
        character.save()
        return redirect('character-detail', pk=character.pk)
    return render(request, 'rpg/character_form.html', {'form': form})


@login_required
def character_detail(request, pk):
    character = get_object_or_404(
        Character.objects.select_related('ruleset', 'campaign'),
        pk=pk,
        owner=request.user,
    )
    recent_rolls = character.rolls.filter(user=request.user).select_related('ruleset')[:8]
    journal_entries = character.journal_entries.filter(user=request.user).select_related('campaign')[:5]
    roll_form = RollForm(user=request.user, initial={'character': character, 'ruleset': character.ruleset})
    journal_form = JournalEntryForm(
        user=request.user,
        initial={'character': character, 'campaign': character.campaign},
    )
    return render(
        request,
        'rpg/character_detail.html',
        {
            'character': character,
            'recent_rolls': recent_rolls,
            'journal_entries': journal_entries,
            'roll_form': roll_form,
            'journal_form': journal_form,
        },
    )


@login_required
def character_edit(request, pk):
    character = get_object_or_404(Character, pk=pk, owner=request.user)
    form = CharacterForm(request.POST or None, user=request.user, instance=character)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('character-detail', pk=character.pk)
    return render(request, 'rpg/character_form.html', {'form': form, 'character': character})


@login_required
@require_POST
def roll_create(request):
    data = request.POST.copy()
    preset = data.get('preset')
    if preset in ROLL_PRESETS:
        preset_label, preset_expression = ROLL_PRESETS[preset]
        data['expression'] = preset_expression
        if not data.get('label'):
            data['label'] = preset_label
    form = RollForm(data, user=request.user)
    roll = None
    error = None
    if form.is_valid():
        try:
            result = roll_expression(form.cleaned_data['expression'])
            character = form.cleaned_data.get('character')
            ruleset = character.ruleset if character else form.cleaned_data['ruleset']
            roll = Roll.objects.create(
                user=request.user,
                ruleset=ruleset,
                character=character,
                campaign=character.campaign if character else None,
                label=form.cleaned_data.get('label', ''),
                context=form.cleaned_data.get('context', ''),
                expression=result['expression'],
                total=result['total'],
                result=result,
            )
        except DiceExpressionError as exc:
            error = str(exc)
    else:
        error = 'Sprawdź zapis rzutu i spróbuj ponownie.'

    if request.headers.get('HX-Request'):
        recent_rolls = Roll.objects.filter(user=request.user).select_related('ruleset', 'character')[:8]
        return render(
            request,
            'rpg/partials/roll_workspace.html',
            {'roll': roll, 'error': error, 'recent_rolls': recent_rolls},
        )
    return redirect('dashboard')


@login_required
@require_POST
def journal_create(request):
    form = JournalEntryForm(request.POST, user=request.user)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.user = request.user
        entry.save()
    if request.headers.get('HX-Request'):
        journal_entries = JournalEntry.objects.filter(user=request.user).select_related('campaign', 'character')[:5]
        return render(
            request,
            'rpg/partials/journal_list.html',
            {'journal_entries': journal_entries},
        )
    return redirect('dashboard')
