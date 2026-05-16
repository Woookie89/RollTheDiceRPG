from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Campaign, Character, Roll, Ruleset
from .serializers import CampaignSerializer, CharacterSerializer, RollSerializer, RulesetSerializer
from .services.dice import roll_expression


class RulesetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ruleset.objects.filter(is_active=True)
    serializer_class = RulesetSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Campaign.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        campaign = serializer.save(owner=self.request.user)
        campaign.members.create(user=self.request.user, role='game_master')


class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Character.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        campaign = serializer.validated_data.get('campaign')
        if campaign:
            if campaign.owner != self.request.user:
                raise PermissionDenied('You can only add characters to your campaigns.')
            serializer.save(owner=self.request.user, ruleset=campaign.ruleset)
        else:
            serializer.save(owner=self.request.user)


class RollViewSet(viewsets.ModelViewSet):
    serializer_class = RollSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Roll.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        expression = serializer.validated_data['expression']
        character = serializer.validated_data.get('character')
        campaign = serializer.validated_data.get('campaign')
        if character and character.owner != self.request.user:
            raise PermissionDenied('You can only roll for your characters.')
        if campaign and campaign.owner != self.request.user:
            raise PermissionDenied('You can only roll in your campaigns.')
        ruleset = character.ruleset if character else serializer.validated_data['ruleset']
        result = roll_expression(expression)
        serializer.save(
            user=self.request.user,
            ruleset=ruleset,
            campaign=character.campaign if character else campaign,
            total=result['total'],
            result=result,
            expression=result['expression'],
        )
