from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from api.permissions import IsAdmin
from api.serializers import (
    UserSerializer, UserMeSerializer
)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    lookup_field = 'username'  # users/{username}/
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options'
    ]

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(IsAuthenticated, ),
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserMeSerializer(
                request.user,
                context=self.get_serializer_context()
            )
            return Response(serializer.data)

        serializer = UserMeSerializer(
            request.user,
            data=request.data,
            partial=True,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
