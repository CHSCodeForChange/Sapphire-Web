from accounts.models import Profile


def profile(request):
	return {'profile': Profile.objects.get(user=request.user)}