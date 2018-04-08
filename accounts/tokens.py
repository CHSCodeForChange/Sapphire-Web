from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

# Makes a hash value for the unique Registration Token
# Extends a PasswordResetTokenGenerator and makes a hash value to use as a url
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) +  six.text_type(user.is_active)

account_activation_token = AccountActivationTokenGenerator()
