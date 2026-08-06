from django.db import migrations


def polish_year_zero_name(apps, schema_editor):
    Ruleset = apps.get_model('rpg', 'Ruleset')
    Ruleset.objects.filter(slug='year-zero').update(
        name='Year Zero / Tajemnice Pętli i Powodzi',
    )


def unpolish_year_zero_name(apps, schema_editor):
    Ruleset = apps.get_model('rpg', 'Ruleset')
    Ruleset.objects.filter(slug='year-zero').update(
        name='Year Zero / Tajemnice Petli i Powodzi',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0002_roll_context_alter_campaignmember_role_journalentry'),
    ]

    operations = [
        migrations.RunPython(polish_year_zero_name, unpolish_year_zero_name),
    ]
