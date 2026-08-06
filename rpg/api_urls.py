from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import CampaignViewSet, CharacterViewSet, JournalEntryViewSet, RollViewSet, RulesetViewSet

router = DefaultRouter()
router.register('rulesets', RulesetViewSet, basename='api-ruleset')
router.register('campaigns', CampaignViewSet, basename='api-campaign')
router.register('characters', CharacterViewSet, basename='api-character')
router.register('rolls', RollViewSet, basename='api-roll')
router.register('journal', JournalEntryViewSet, basename='api-journal')

urlpatterns = [
    path('', include(router.urls)),
]
