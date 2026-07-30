from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.constants import EMAIL_FIELD_LENGTH, USERNAME_FIELD_LENGTH
from users.validators import username_not_me


username_validation = UnicodeUsernameValidator()


User = get_user_model()


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=EMAIL_FIELD_LENGTH)
    username = serializers.CharField(
        max_length=USERNAME_FIELD_LENGTH,
        validators=(username_validation, username_not_me),
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        user_by_name = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_name and user_by_email and user_by_name != user_by_email:
            raise serializers.ValidationError(
                {'email': 'Этот email занят другим пользователем.'}
            )
        if user_by_email and not user_by_name:
            raise serializers.ValidationError(
                {'email': 'Этот email уже зарегистрирован.'}
            )
        if user_by_name and not user_by_email:
            raise serializers.ValidationError(
                {'username': 'Этот username уже занят с другим email.'}
            )
        return data

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(
            username=validated_data['username'],
            defaults={'email': validated_data['email']}
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='YaMDb — код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_FIELD_LENGTH,
        validators=(username_validation, ),
    )
    confirmation_code = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
            user,
            data['confirmation_code']
        ):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный или устаревший код.'}
            )
        data['user'] = user
        return data
