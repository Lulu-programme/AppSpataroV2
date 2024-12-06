sector = [
    'Parking',
    'Lavage',
    'Chimie',
    'Gaz',
    'Distribution',
]
country = [
    'Belgique',
    'France',
    'Allemagne',
    'Pays-Bas',
    'Italie',
    'Suisse',
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

def change_text_to_list(to_change):
    changed = []
    last_modified = 0
    for i in range(len(to_change)):
        if to_change[i] == ',' or to_change[i] == '.':
            word = to_change[last_modified:i]
            cap_word = word.strip().capitalize() + '.'
            changed.append(cap_word)
            last_modified = i + 2
    return changed

def change_list_to_text(to_change):
    return ', '.join([change for change in to_change])