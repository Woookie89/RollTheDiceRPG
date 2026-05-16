from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import CampaignViewSet, CharacterViewSet, RollViewSet, RulesetViewSet

router = DefaultRouter()
router.register('rulesets', RulesetViewSet, basename='ruleset')
router.register('campaigns', CampaignViewSet, basename='campaign')
router.register('characters', CharacterViewSet, basename='character')
router.register('rolls', RollViewSet, basename='roll')

urlpatterns = [
    path('', include(router.urls)),
]
