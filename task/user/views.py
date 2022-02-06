from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserPublicSerializer, UserSerializer

User = get_user_model()


class UserView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserPublicSerializer(queryset, many=True)
        return Response({
            "success": True,
            "response": serializer.data
        })

    def put(self, request, *args, **kwargs):
        try:
            if hasattr(self.request, 'user') and not request.user.is_anonymous:
                user = User.objects.get(id=self.request.user.id)
                serializer = UserSerializer(user, data=self.request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                result = UserSerializer(user).data
                return Response({
                    "success": True,
                    "response": result
                })
            else:
                return Response({
                    "success": False,
                    "error": "Not authorised for this action!"},
                    status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            raise ValidationError(e)
