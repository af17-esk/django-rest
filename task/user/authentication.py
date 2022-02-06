from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import exceptions
from django.utils.translation import ugettext as _
from django.contrib.auth.backends import BaseBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication, jwt_get_username_from_payload

User = get_user_model()


class EmailBackend(BaseBackend):

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None


class CustomJsonWebTokenAuthentication(JSONWebTokenAuthentication):

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        User = get_user_model()
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user
