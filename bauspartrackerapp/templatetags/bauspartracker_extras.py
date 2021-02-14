from django import template
register = template.Library()

@register.filter
def percentage( value, arg ):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        percentage = float( arg )
        if percentage: return round(value / 100 * percentage, 2)
    except: pass
    return ''