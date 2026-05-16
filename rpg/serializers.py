from rest_framework import serializers

from .models import Campaign, Character, Roll, Ruleset


class RulesetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruleset
        fields = ('slug', 'name', 'family', 'primary_die', 'theme', 'dice', 'terms')


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('id', 'name', 'slug', 'description', 'ruleset', 'created_at', 'updated_at')
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('id', 'name', 'campaign', 'ruleset', 'portrait', 'data', 'notes', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class RollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roll
        fields = ('id', 'ruleset', 'campaign', 'character', 'label', 'expression', 'total', 'result', 'created_at')
        read_only_fields = ('id', 'total', 'result', 'created_at')
