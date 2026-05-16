from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Campaign, Character, JournalEntry, Roll, Ruleset
from .serializers import (
    CampaignSerializer,
    CharacterSerializer,
    JournalEntrySerializer,
    RollSerializer,
    RulesetSerializer,
)
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

    def retrieve(self, request, *args, **kwargs):
        campaign = self.get_object()
        if request.accepted_renderer.format in ['api', 'html']:
            return redirect('campaign-detail', pk=campaign.pk)
        serializer = self.get_serializer(campaign)
        return Response(serializer.data)


class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Character.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        campaign = serializer.validated_data.get('campaign')
        if campaign:
            if campaign.owner != self.request.user:
                raise PermissionDenied('Możesz dodawać postacie tylko do swoich kampanii.')
            serializer.save(owner=self.request.user, ruleset=campaign.ruleset)
        else:
            serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        campaign = serializer.validated_data.get('campaign', serializer.instance.campaign)
        if campaign and campaign.owner != self.request.user:
            raise PermissionDenied('Możesz przypisywać postacie tylko do swoich kampanii.')
        if campaign:
            serializer.save(ruleset=campaign.ruleset)
        else:
            serializer.save()

    def retrieve(self, request, *args, **kwargs):
        character = self.get_object()
        if request.accepted_renderer.format in ['api', 'html']:
            return redirect('character-detail', pk=character.pk)
        serializer = self.get_serializer(character)
        return Response(serializer.data)


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
            raise PermissionDenied('Możesz rzucać tylko dla swoich postaci.')
        if campaign and campaign.owner != self.request.user:
            raise PermissionDenied('Możesz rzucać tylko w swoich kampaniach.')
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


class JournalEntryViewSet(viewsets.ModelViewSet):
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        campaign = serializer.validated_data.get('campaign')
        character = serializer.validated_data.get('character')
        if campaign and campaign.owner != self.request.user:
            raise PermissionDenied('Możesz dodawać wpisy tylko do swoich kampanii.')
        if character and character.owner != self.request.user:
            raise PermissionDenied('Możesz dodawać wpisy tylko do swoich postaci.')
        serializer.save(user=self.request.user)
