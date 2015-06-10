from django import template

register = template.Library()


@register.filter()
def interval(time_delta):
    sec = time_delta.total_seconds()
    hours, remainder = divmod(sec, 3600)
    minutes, sec = divmod(remainder, 60)
    return '%4d:%02d' % (int(hours), int(minutes))
