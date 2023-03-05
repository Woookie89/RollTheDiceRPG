from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name', 'last_name', 'bio', 'city', 'postal_code', 'country', 'avatar')

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            name=validated_data['name'],
            last_name=validated_data['last_name'],
            bio=validated_data['bio'],
            city=validated_data['city'],
            postal_code=validated_data['postal_code'],
            country=validated_data['country'],
            avatar=validated_data['avatar'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
