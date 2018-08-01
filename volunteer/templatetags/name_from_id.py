from django import template
from django.contrib.auth.models import User

from groups.models import Group

register = template.Library()


@register.tag
def group_name_from_id(ids):
	full_string = ""
	for group_id in str.split(ids, "_"):
		if group_id == "":
			continue
		try:
			full_string += Group.objects.get(pk=group_id).name + ", "
		except Group.DoesNotExist:
			return "No Such Group"
	# This expression removes the last ", " from the string
	return full_string[:-2]


@register.tag
def format_daterange(daterange):
	try:
		start, end = str.split(daterange, "_")
		year_s, month_s, day_s = str.split(start, "-")
		year_e, month_e, day_e = str.split(end, "-")
		return month_s + "/" + day_s + "/" + year_s + " to " + month_e + "/" + day_e + "/" + year_e
	except ValueError:
		return daterange


register.filter('group_name_from_id', group_name_from_id)
register.filter('format_daterange', format_daterange)
