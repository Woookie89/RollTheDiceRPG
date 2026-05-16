from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Ruleset(models.Model):
    slug = models.SlugField(primary_key=True, max_length=64)
    name = models.CharField(max_length=120)
    family = models.CharField(max_length=80, blank=True)
    primary_die = models.CharField(max_length=16, blank=True)
    theme = models.CharField(max_length=80, default='neutral')
    dice = models.JSONField(default=list)
    terms = models.JSONField(default=dict)
    sort_order = models.PositiveSmallIntegerField(default=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Campaign(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='owned_campaigns',
        on_delete=models.CASCADE,
    )
    ruleset = models.ForeignKey(Ruleset, related_name='campaigns', on_delete=models.PROTECT)
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = [('owner', 'slug')]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CampaignMember(models.Model):
    PLAYER = 'player'
    GAME_MASTER = 'game_master'

    ROLE_CHOICES = [
        (PLAYER, 'Gracz'),
        (GAME_MASTER, 'Mistrz Gry'),
    ]

    campaign = models.ForeignKey(Campaign, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='campaign_memberships', on_delete=models.CASCADE)
    role = models.CharField(max_length=24, choices=ROLE_CHOICES, default=PLAYER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('campaign', 'user')]

    def __str__(self):
        return f'{self.user} in {self.campaign}'


class Character(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='characters', on_delete=models.CASCADE)
    campaign = models.ForeignKey(
        Campaign,
        related_name='characters',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    ruleset = models.ForeignKey(Ruleset, related_name='characters', on_delete=models.PROTECT)
    name = models.CharField(max_length=120)
    portrait = models.ImageField(upload_to='characters', blank=True, null=True)
    data = models.JSONField(default=dict, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def sheet_fields(self):
        from .services.character_presets import iter_character_fields

        return iter_character_fields(self.data)


class Roll(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rolls', on_delete=models.CASCADE)
    ruleset = models.ForeignKey(Ruleset, related_name='rolls', on_delete=models.PROTECT)
    campaign = models.ForeignKey(Campaign, related_name='rolls', null=True, blank=True, on_delete=models.SET_NULL)
    character = models.ForeignKey(Character, related_name='rolls', null=True, blank=True, on_delete=models.SET_NULL)
    label = models.CharField(max_length=120, blank=True)
    context = models.CharField(max_length=160, blank=True)
    expression = models.CharField(max_length=80)
    total = models.IntegerField(null=True, blank=True)
    result = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.label or self.expression


class JournalEntry(models.Model):
    NOTE = 'note'
    SESSION = 'session'
    EVENT = 'event'
    REWARD = 'reward'

    TYPE_CHOICES = [
        (NOTE, 'Notatka'),
        (SESSION, 'Sesja'),
        (EVENT, 'Wydarzenie'),
        (REWARD, 'Nagroda'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='journal_entries', on_delete=models.CASCADE)
    campaign = models.ForeignKey(
        Campaign,
        related_name='journal_entries',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    character = models.ForeignKey(
        Character,
        related_name='journal_entries',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    entry_type = models.CharField(max_length=24, choices=TYPE_CHOICES, default=NOTE)
    title = models.CharField(max_length=140)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'wpis dziennika'
        verbose_name_plural = 'wpisy dziennika'

    def __str__(self):
        return self.title
