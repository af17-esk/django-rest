from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('designation', )


class UserSerializer(serializers.ModelSerializer):

    user_profile = UserProfileSerializer(many=True, required=False, source="profile")

    def update(self, instance, validated_data):
        profile = validated_data.pop("profile", None)
        user = super().update(instance, validated_data)
        if profile:
            user.profile.all().delete()
            UserProfile.objects.bulk_create(
                [
                    UserProfile(user=instance, **profile)
                    for profile in profile
                ],
            )
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'phone_number', 'birth_date',
                  'created_at', 'updated_at', 'gender', 'user_profile', )
        read_only_fields = ('id', 'email', 'created_at', 'gender')
        extra_kwargs = {
            "user_profile": {
                "read_only": False,
                "required": False,
            },
        }


class UserPublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'name', 'gender', )
