from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retourne la valeur d'une clé dans un dictionnaire"""
    return dictionary.get(key)

@register.filter
def key_exists(dictionary, key):
    """Vérifie si une clé existe dans un dictionnaire"""
    return key in dictionary
