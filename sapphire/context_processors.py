from accounts.models import Profile


def profile(request):
	if request.user.is_authenticated():
		return {'profile': Profile.objects.get(user=request.user)}
	else:
		return {'profile': None}
