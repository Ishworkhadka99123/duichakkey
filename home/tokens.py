from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class PaymentConfirmationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)
        )