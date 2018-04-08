from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()


# This tag *must* be passed a set of user_slot objects or it will fail to call is_volunteer_null()
@register.filter(name='volunteer_count')
def volunteer_count(user_slot_set):
  total = 0
  for user_slot in user_slot_set:
    if not user_slot.is_volunteer_null():
      total += 1
  return total
