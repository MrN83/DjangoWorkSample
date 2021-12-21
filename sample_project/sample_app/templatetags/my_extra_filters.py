from django import template

register = template.Library()

#Using decorator, passing appendText into register.filter() as a function with a parameter.
@register.filter(name="appendText")
def appendText(value, arg):

    '''
    Appends arg to value
    '''
    if value is None:
        return arg
    else:
        return arg + value

#Without using decorator
# register.filter('appendText', appendText)
