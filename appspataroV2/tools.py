sector_list = [
    'Parking',
    'Lavage',
    'Chimie',
    'Gaz',
    'Distribution',
]
country_list = [
    'Belgique',
    'France',
    'Allemagne',
    'Pays-Bas',
    'Italie',
    'Suisse',
]
provision_list = [
    'Café',
    'Douche',
    'Toilette',
    'Distributeur',
    'Salle d\'attente',
]
language_list = [
    'Français',
    'Anglais',
    'Néerlandais',
    'Allemand',
    'Italien',
    'Espagnol',
    'Polonais',
]
reception_list = [
    'Sympathique',
    'Correct',
    'Inexistant',
]
labels_list = [
    '2.1',
    '2.2',
    '2.3',
    '3',
    '4.1',
    '4.2',
    '4.3',
    '5.1',
    '5.2',
    '6.1',
    '6.2',
    '8',
    '9',
    'Environnement',
    'Température',
]

def description_p(description):
    paragraph = []
    last_point = 0
    for i in range(len(description)):
        if description[i] == '.':
            para = description[last_point:i]
            para = para.replace('(', '<span class="marked">(')
            para = para.replace(')', ')</span>')
            cap_para = para.strip().capitalize()
            paragraph.append(cap_para + '.')
            last_point = i + 1
    return paragraph

def change_text_to_list(to_change, final):
    changed = []
    last_modified = 0
    for i in range(len(to_change)):
        if to_change[i] == ',' or to_change[i] == final:
            word = to_change[last_modified:i]
            cap_word = word.strip().capitalize()
            changed.append(cap_word)
            last_modified = i + 1
    return changed

def change_list_to_text(to_change, last):
    return ', '.join([change for change in to_change]) + last

def zip_town(country, zip_code, town):
    if country.upper() == 'PAYS-BAS':
        code = 'NL'
    elif country.upper() == 'ITALIE':
        code = 'IT'
    elif country.upper() == 'ALLEMAGNE':
        code = 'D'
    elif country.upper() == 'SUISSE':
        code = 'CH'
    else:
        code = country[0]
    return f'{code} - {zip_code} {town}'