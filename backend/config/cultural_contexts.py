"""
Cultural Contexts Configuration for MediTalks
Defines available cultural contexts and their properties
"""

CULTURAL_CONTEXTS = [
    {
        'value': 'tagalog-rural',
        'label': 'Tagalog (Rural Philippines)',
        'language': 'Tagalog/Filipino',
        'region': 'Philippines',
        'description': 'Rural Filipino communities with traditional family values',
        'characteristics': [
            'Strong family orientation',
            'Respect for elders',
            'Community-based healthcare decisions',
            'Traditional healing practices awareness',
            'Catholic religious influences'
        ]
    },
    {
        'value': 'thai-low-literacy',
        'label': 'Thai (Low Literacy)',
        'language': 'Thai',
        'region': 'Thailand',
        'description': 'Thai communities with limited literacy levels',
        'characteristics': [
            'Buddhist cultural influences',
            'Preference for simple language',
            'Visual and metaphorical communication',
            'Traditional medicine integration',
            'Respectful hierarchical communication'
        ]
    },
    {
        'value': 'khmer-indigenous',
        'label': 'Khmer (Indigenous Communities)',
        'language': 'Khmer/Cambodian',
        'region': 'Cambodia',
        'description': 'Indigenous Khmer communities with traditional practices',
        'characteristics': [
            'Strong Buddhist beliefs',
            'Traditional healing practices',
            'Community consensus in decisions',
            'Oral tradition communication',
            'Respect for traditional healers'
        ]
    },
    {
        'value': 'vietnamese-elderly',
        'label': 'Vietnamese (Elderly)',
        'language': 'Vietnamese',
        'region': 'Vietnam',
        'description': 'Elderly Vietnamese population with traditional values',
        'characteristics': [
            'Confucian hierarchical values',
            'Family-centered healthcare decisions',
            'Traditional medicine integration',
            'Formal and respectful communication',
            'Intergenerational healthcare involvement'
        ]
    },
    {
        'value': 'malay-traditional',
        'label': 'Malay (Traditional Communities)',
        'language': 'Malay/Bahasa Melayu',
        'region': 'Malaysia/Indonesia',
        'description': 'Traditional Malay communities with Islamic influences',
        'characteristics': [
            'Islamic religious considerations',
            'Family and community involvement',
            'Halal healthcare considerations',
            'Respectful gender-appropriate communication',
            'Traditional and modern medicine integration'
        ]
    }
]

# Quick lookup dictionary
CONTEXT_LOOKUP = {context['value']: context for context in CULTURAL_CONTEXTS}

# Supported languages
SUPPORTED_LANGUAGES = [
    {'code': 'en', 'name': 'English', 'native_name': 'English'},
    {'code': 'th', 'name': 'Thai', 'native_name': 'ไทย'},
    {'code': 'vi', 'name': 'Vietnamese', 'native_name': 'Tiếng Việt'},
    {'code': 'ms', 'name': 'Malay', 'native_name': 'Bahasa Melayu'},
    {'code': 'km', 'name': 'Khmer', 'native_name': 'ខ្មែរ'},
    {'code': 'tl', 'name': 'Tagalog', 'native_name': 'Filipino'}
]

# Language lookup
LANGUAGE_LOOKUP = {lang['code']: lang for lang in SUPPORTED_LANGUAGES}
