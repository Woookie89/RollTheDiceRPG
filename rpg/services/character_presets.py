PRESET_FIELDS = {
    'dnd5e': {
        'role_label': 'Klasa',
        'origin_label': 'Pochodzenie',
        'resource_label': 'Klasa pancerza',
        'health_label': 'Punkty wytrzymałości',
        'level_label': 'Poziom',
        'default_expression': '1d20',
    },
    'call-of-cthulhu': {
        'role_label': 'Profesja',
        'origin_label': 'Organizacja / pochodzenie',
        'resource_label': 'Poczytalność',
        'health_label': 'Punkty wytrzymałości',
        'level_label': 'Szczęście',
        'default_expression': '1d100',
    },
    'year-zero': {
        'role_label': 'Archetyp',
        'origin_label': 'Motywacja',
        'resource_label': 'Kondycja',
        'health_label': 'Stan zdrowia',
        'level_label': 'Wiek',
        'default_expression': '6d6',
    },
    'warhammer-4e': {
        'role_label': 'Profesja',
        'origin_label': 'Pochodzenie',
        'resource_label': 'Przewaga',
        'health_label': 'Rany',
        'level_label': 'Poziom kariery',
        'default_expression': '1d100',
    },
    'vampire-v5': {
        'role_label': 'Klan',
        'origin_label': 'Maska / koncepcja',
        'resource_label': 'Głód',
        'health_label': 'Zdrowie',
        'level_label': 'Człowieczeństwo',
        'default_expression': '5d10',
    },
    'kult': {
        'role_label': 'Archetyp',
        'origin_label': 'Mroczny sekret',
        'resource_label': 'Stabilność',
        'health_label': 'Rany',
        'level_label': 'Relacje',
        'default_expression': '2d10',
    },
}

DEFAULT_PRESET = {
    'role_label': 'Archetyp / rola',
    'origin_label': 'Pochodzenie / motywacja',
    'resource_label': 'Zasób główny',
    'health_label': 'Stan zdrowia',
    'level_label': 'Poziom / etap',
    'default_expression': '1d20',
}


def get_preset(ruleset_slug):
    return PRESET_FIELDS.get(ruleset_slug, DEFAULT_PRESET)


def build_character_data(ruleset_slug, values):
    preset = get_preset(ruleset_slug)
    return {
        'role': {
            'label': preset['role_label'],
            'value': values.get('role', ''),
        },
        'origin': {
            'label': preset['origin_label'],
            'value': values.get('origin', ''),
        },
        'level': {
            'label': preset['level_label'],
            'value': values.get('level', ''),
        },
        'resource': {
            'label': preset['resource_label'],
            'value': values.get('resource', ''),
        },
        'health': {
            'label': preset['health_label'],
            'value': values.get('health', ''),
        },
        'default_expression': preset['default_expression'],
    }


def flatten_character_data(data):
    return {
        'role': data.get('role', {}).get('value', ''),
        'origin': data.get('origin', {}).get('value', ''),
        'level': data.get('level', {}).get('value', ''),
        'resource': data.get('resource', {}).get('value', ''),
        'health': data.get('health', {}).get('value', ''),
    }


def iter_character_fields(data):
    fields = []
    for key in ['role', 'origin', 'level', 'resource', 'health']:
        item = data.get(key, {})
        if item.get('value'):
            fields.append(item)
    return fields
