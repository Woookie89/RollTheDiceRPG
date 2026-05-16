from rest_framework import serializers

from .models import Campaign, Character, JournalEntry, Roll, Ruleset


class RulesetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruleset
        fields = ('slug', 'name', 'family', 'primary_die', 'theme', 'dice', 'terms')


class CampaignSerializer(serializers.ModelSerializer):
    view_url = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = ('id', 'name', 'slug', 'description', 'ruleset', 'view_url', 'created_at', 'updated_at')
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')

    def get_view_url(self, obj):
        return f'/campaigns/{obj.pk}/'


class CharacterSerializer(serializers.ModelSerializer):
    view_url = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = ('id', 'name', 'campaign', 'ruleset', 'view_url', 'portrait', 'data', 'notes', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_view_url(self, obj):
        return f'/characters/{obj.pk}/'


class RollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roll
        fields = ('id', 'ruleset', 'campaign', 'character', 'label', 'context', 'expression', 'total', 'result', 'created_at')
        read_only_fields = ('id', 'total', 'result', 'created_at')


class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ('id', 'campaign', 'character', 'entry_type', 'title', 'body', 'created_at')
        read_only_fields = ('id', 'created_at')
