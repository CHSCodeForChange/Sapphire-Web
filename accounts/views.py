from email.mime.image import MIMEImage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from .models import Profile
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from feed.models import Feed_Entry
from groups.models import Group
from django.contrib.auth import update_session_auth_hash
from alerts.models import Alert




# Redirects to the profile page
def home(request):
    redirect('accounts/profile')

# The profile page for the current user
def profile(request):
    if request.user.is_authenticated():
        # This line breaks the code: "'int' is not iterable"
        user = request.user
        profile = user.profile
        groups = Group.get_is_member_list(request.user)

        feed_entries = Feed_Entry.objects.filter(user=user).order_by('-datetime')[:10]
        return render(request, "accounts/profile.html", {'user':user, 'profile':profile,'feed_entries':feed_entries, 'this_user':True, 'groups':groups})
    else:
        return redirect('/login')
def other_profile(request, user_id):
    user = User.objects.get(id=user_id)
    if (user != request.user):
        profile = Profile.objects.get(user=user)
        groups = Group.get_is_member_list(user)
        feed_entries = Feed_Entry.objects.filter(user=request.user).order_by('-datetime')[:10]
        return render(request, 'accounts/profile.html', {'user':user, 'profile':profile,'feed_entries':feed_entries, 'this_user':False, 'groups':groups})
    else:
        return redirect('/accounts/profile')

def edit_profile(request):
    profile = request.user.profile
    if request.POST:
        form = EditProfileForm(request.POST, profile=profile)
        form2 = EditUserForm(request.POST, instance=request.user)
        if form.is_valid() and form2.is_valid():
            profile.bio = form.save(commit=False)
            profile.save()
            form2.save()

            alert = Alert(user=request.user, text="Profile updated", color=Alert.getYellow())
            alert.saveIP(request)

            return redirect('/accounts/profile/')
    form = EditProfileForm(initial={'bio':profile.bio})
    form2 = EditUserForm(instance=request.user)


    return render(request, 'accounts/edit_profile.html', {"form":form, 'profile':profile, "form2": form2})

def edit_password(request):
    user = request.user
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.POST:
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            alert = Alert(user=request.user, text="Password updated", color=Alert.getYellow())
            alert.saveIP(request)

            return redirect('/accounts/profile')

    return render(request, 'accounts/edit_password.html', {"form":form})

# The signup page
def signup(request):
    # Checks if the user is sending their data (POST) or getting the form (GET)
    if(request.method == 'POST'):
        form = SignupForm(request.POST)
        # Makes sure the user filled out the form correctly as dictated by forms.py
        if form.is_valid():
            user = form.save(commit=False)
            # Sets the user to deactive until they confirm email
            user.is_active = False
            # Saves the user to the server
            user.save()
            # Gets the current domain in order to send the email
            current_site = get_current_site(request)
            # Sends the user an email based on the email template and the info passed in here
            message = render_to_string('emails/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your Sapphire Account!'
            to_email = form.cleaned_data.get('email')
            email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
            email.content_subtype = 'html'
            email.mixed_subtype = 'related'
            fp = open('static/img/logos.ico/WithText.jpg', 'rb')
            logo = MIMEImage(fp.read())
            logo.add_header('Content-ID', '<logo>')
            email.attach(logo)
            email.send()
            return render(request, 'accounts/please_confirm.html')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

# The activation page for new users
# The uidb64 and token are generated in signup
def activate(request, uidb64, token):
    # Tries to decode the uid and use it as a key to find a user
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        # Sets the profile's primary key to be the same as the user's
        profile = Profile(username = user.get_username())
    # Catches if the activation link is bad
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        # Sets the user to active
        user.is_active = True
        user.save()
        #profile.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return render(request, 'accounts/account_confirmed.html')
    else:
        return HttpResponse('Activation link is invalid!')

def logoutLander(request):
    alert = Alert(text="You logged out", color=Alert.getRed())
    alert.saveIP(request)

    return redirect('/login')
    #return render(request, 'accounts/logout_lander.html')
