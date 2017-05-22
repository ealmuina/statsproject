from django import template

register = template.Library()


@register.filter(name='matched_user')
def matched_user(match, user):
    return match.matched_user(user.id)
