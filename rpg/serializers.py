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
    ruleset_detail = serializers.SerializerMethodField()
    recent_rolls = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = (
            'id',
            'name',
            'campaign',
            'ruleset',
            'ruleset_detail',
            'view_url',
            'portrait',
            'data',
            'notes',
            'is_active',
            'recent_rolls',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_view_url(self, obj):
        return f'/characters/{obj.pk}/'

    def get_ruleset_detail(self, obj):
        return RulesetSerializer(obj.ruleset).data

    def get_recent_rolls(self, obj):
        return [
            {
                'id': roll.pk,
                'label': roll.label,
                'context': roll.context,
                'expression': roll.expression,
                'total': roll.total,
                'result': roll.result,
                'created_at': roll.created_at,
            }
            for roll in obj.rolls.all()[:5]
        ]


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
