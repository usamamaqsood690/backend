from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        import secrets
        from .models import UserProfile
        
        user = User.objects.create_user(
            username=validated_data['email'],  # 👈 username becomes email
            email=validated_data['email'],
            password=validated_data['password']
        )
        UserProfile.objects.get_or_create(
            user=user,
            defaults={'mongo_id': secrets.token_hex(12)}
        )
        return user


class RegisterResponseSerializer(serializers.ModelSerializer):
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'access', 'refresh']

    def get_access(self, obj):
        return str(RefreshToken.for_user(obj).access_token)

    def get_refresh(self, obj):
        return str(RefreshToken.for_user(obj))