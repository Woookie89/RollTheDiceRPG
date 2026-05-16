from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import CampaignForm, CharacterForm, RollForm
from .models import Campaign, Character, Roll, Ruleset
from .services.dice import DiceExpressionError, roll_expression


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    rulesets = Ruleset.objects.filter(is_active=True)[:6]
    return render(request, 'rpg/landing.html', {'rulesets': rulesets})


@login_required
def dashboard(request):
    characters = Character.objects.filter(owner=request.user).select_related('ruleset', 'campaign')
    campaigns = Campaign.objects.filter(owner=request.user).select_related('ruleset')
    recent_rolls = Roll.objects.filter(user=request.user).select_related('ruleset', 'character')[:8]
    form = RollForm(user=request.user)
    return render(
        request,
        'rpg/dashboard.html',
        {
            'characters': characters,
            'campaigns': campaigns,
            'recent_rolls': recent_rolls,
            'roll_form': form,
        },
    )


@login_required
def campaign_create(request):
    form = CampaignForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        campaign = form.save(commit=False)
        campaign.owner = request.user
        campaign.save()
        campaign.members.create(user=request.user, role='game_master')
        return redirect('dashboard')
    return render(request, 'rpg/campaign_form.html', {'form': form})


@login_required
def character_create(request):
    form = CharacterForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        character = form.save(commit=False)
        character.owner = request.user
        if character.campaign_id:
            character.ruleset = character.campaign.ruleset
        character.save()
        return redirect('dashboard')
    return render(request, 'rpg/character_form.html', {'form': form})


@login_required
@require_POST
def roll_create(request):
    form = RollForm(request.POST, user=request.user)
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
                expression=result['expression'],
                total=result['total'],
                result=result,
            )
        except DiceExpressionError as exc:
            error = str(exc)
    else:
        error = 'Sprawdz zapis rzutu i sproboj ponownie.'

    if request.headers.get('HX-Request'):
        return render(request, 'rpg/partials/roll_result.html', {'roll': roll, 'error': error})
    return redirect('dashboard')
