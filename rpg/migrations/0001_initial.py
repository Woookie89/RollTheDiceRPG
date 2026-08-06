from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

from rpg.services.rulesets import RULESETS


def seed_rulesets(apps, schema_editor):
    Ruleset = apps.get_model('rpg', 'Ruleset')
    for ruleset in RULESETS:
        data = ruleset.copy()
        slug = data.pop('slug')
        Ruleset.objects.update_or_create(
            slug=slug,
            defaults=data,
        )


def unseed_rulesets(apps, schema_editor):
    Ruleset = apps.get_model('rpg', 'Ruleset')
    Ruleset.objects.filter(slug__in=[ruleset['slug'] for ruleset in RULESETS]).delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ruleset',
            fields=[
                ('slug', models.SlugField(max_length=64, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('family', models.CharField(blank=True, max_length=80)),
                ('primary_die', models.CharField(blank=True, max_length=16)),
                ('theme', models.CharField(default='neutral', max_length=80)),
                ('dice', models.JSONField(default=list)),
                ('terms', models.JSONField(default=dict)),
                ('sort_order', models.PositiveSmallIntegerField(default=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['sort_order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True, max_length=140)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_campaigns', to=settings.AUTH_USER_MODEL)),
                ('ruleset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='campaigns', to='rpg.ruleset')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('owner', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('portrait', models.ImageField(blank=True, null=True, upload_to='characters')),
                ('data', models.JSONField(blank=True, default=dict)),
                ('notes', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='characters', to='rpg.campaign')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characters', to=settings.AUTH_USER_MODEL)),
                ('ruleset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='characters', to='rpg.ruleset')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CampaignMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('player', 'Player'), ('game_master', 'Game master')], default='player', max_length=24)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='rpg.campaign')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaign_memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('campaign', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Roll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=120)),
                ('expression', models.CharField(max_length=80)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('result', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rolls', to='rpg.campaign')),
                ('character', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rolls', to='rpg.character')),
                ('ruleset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rolls', to='rpg.ruleset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rolls', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.RunPython(seed_rulesets, unseed_rulesets),
    ]
