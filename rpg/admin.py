from django.contrib import admin

from .models import Campaign, CampaignMember, Character, Roll, Ruleset


@admin.register(Ruleset)
class RulesetAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'family', 'primary_die', 'is_active')
    list_filter = ('is_active', 'family')
    search_fields = ('name', 'slug')


class CampaignMemberInline(admin.TabularInline):
    model = CampaignMember
    extra = 0


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'ruleset', 'owner', 'updated_at')
    list_filter = ('ruleset',)
    search_fields = ('name', 'owner__username')
    inlines = [CampaignMemberInline]


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'ruleset', 'owner', 'campaign', 'is_active')
    list_filter = ('ruleset', 'is_active')
    search_fields = ('name', 'owner__username')


@admin.register(Roll)
class RollAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'ruleset', 'label', 'expression', 'total')
    list_filter = ('ruleset',)
    search_fields = ('label', 'expression', 'user__username')
