from django.shortcuts import render
from rest_auth.registration.views import RegisterView
from rest_framework.permissions import AllowAny


class UserRegisterView(RegisterView):

    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def get_response_data(self, user):
        token = jwt_encode(user)
        if hasattr(user, 'chef_profile') and user.chef_profile:
            user = UserGetSerializer(user).data
        elif hasattr(user, 'eater_profile') and user.eater_profile:
            user = EaterGetSerializer(user).data
        result = {'user': user, 'token': token}
        return result
