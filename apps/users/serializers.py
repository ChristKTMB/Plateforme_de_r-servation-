# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['birth_date', 'address']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone', 'user_type', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user

# users/serializers.py (continue)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Identifiants invalides.")
        data['user'] = user
        return data
