from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Ajoute une classe CSS à un champ de formulaire
    Usage: {{ field|add_class:"form-control" }}
    """
    return field.as_widget(attrs={
        "class": f"{field.css_classes()} {css_class}".strip()
    })