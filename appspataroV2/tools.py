import re


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
    'Atelier mécanique',
    'Espace fumeur',
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
months_to_search = [
    'Jan', 
    'Fév', 
    'Mars', 
    'Avr', 
    'Mai', 
    'Juin', 
    'Juil', 
    'Aout', 
    'Sept', 
    'Oct', 
    'Nov', 
    'Déc',
]
months_entries = [
    'Janvier',
    'Février',
    'Mars',
    'Avril',
    'Mai',
    'Juin',
    'Juillet',
    'Aout',
    'Septembre',
    'Octobre',
    'Novembre',
    'Décembre',
]


def convert_seconds(seconds, string):
    """Convertiseur de seconde en minutes

    Args:
        seconds (int): Les secondes totalisés
        string (bool): Pour avoir le résultat au format str ou tuple int

    Returns:
        str: On reçois directement l'heure au format de chaine de caratère
        tuple: On reçois les heures en int et les minutes en int
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if string:
        return f'{hours:02}h{minutes:02}'
    return hours, minutes


def hours_seconds(hours, minutes):
    """On convertit les heures et les minutes en secondes

    Args:
        hours (int): les heures
        minutes (int): Les minutes

    Returns:
        int: Les heures et les minutes calculé et convertis en minute
    """
    return (hours * 3600) + (minutes * 60)


def calculate_laps_time(hour_start, hour_end, minute_start, minute_end, string):
    if hour_end < hour_start or (hour_end == hour_start and minute_end < minute_start):
        hour_end += 24
    second_start = hours_seconds(hour_start, minute_start)
    second_end = hours_seconds(hour_end, minute_end)
    seconds = second_end - second_start
    if string:
        return convert_seconds(seconds, string)
    return seconds


def description_p(description):
    paragraphs = description.split('.')
    formatted = []
    for para in paragraphs:
        para = re.sub(r'\((.*?)\)', r'<span class="marked">(\1)</span>', para.strip())
        if para:
            formatted.append(para.capitalize() + '.')
    return formatted


def change_text_to_list(to_change, cute, final, number):
    changed = []
    last_modified = 0
    for i in range(len(to_change)):
        if to_change[i] == cute or to_change[i] == final:
            if number:
                change = int(to_change[last_modified:i])
            else:
                word = to_change[last_modified:i]
                change = word.strip().capitalize()
            changed.append(change)
            last_modified = i + 1
    return changed


def change_list_to_text(to_change, last):
    return ', '.join([change for change in to_change]) + last


def zip_town(country, zip_code, town):
    country_codes = {
        'PAYS-BAS': 'NL',
        'ITALIE': 'IT',
        'ALLEMAGNE': 'D',
        'SUISSE': 'CH',
    }
    code = country_codes.get(country.upper(), country[0])
    return f'{code} - {zip_code} {town}'


def validate_list(input_string):
    """
    Vérifie si la chaîne donnée est correctement formatée.
    - Chaque commande doit être séparée par une virgule.
    - La chaîne doit se terminer par un point.
    - Une seule commande sans virgule est aussi acceptée.

    Args:
        input_string (str): La chaîne à vérifier.

    Returns:
        bool: True si le format est valide, False sinon.
        str: Message d'erreur en cas de format invalide.
    """
    # Supprimer les espaces inutiles autour de la chaîne
    input_string = input_string.strip()
    
    # Vérification du format
    if not input_string.endswith('.'):
        return "La chaîne doit se terminer par un point (.)."
    
    # Supprimer le point pour la vérification des éléments
    content = input_string[:-1].strip()
    
    # Vérification si une seule commande est présente
    if re.fullmatch(r'\d+', content):
        return "1"

    # Vérification pour plusieurs commandes séparées par des virgules
    if re.fullmatch(r'(\d+, )*\d+', content):
        return "+"
