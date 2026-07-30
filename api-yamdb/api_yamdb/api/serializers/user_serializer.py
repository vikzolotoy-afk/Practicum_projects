from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserMeSerializer(UserSerializer):
    """
    Сериализатор для /me/.
    role — только чтение, пользователь не может менять свою роль.
    """
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role', )
