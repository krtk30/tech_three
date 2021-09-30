from django.contrib.auth.admin import sensitive_post_parameters_m
from django.utils.translation import ugettext_lazy as _
# Create your views here.
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from account.models import User, Mode, Role
from account.serializers import LoginSerializer, UserSerializer, ChangePasswordSerializer, RoleSerializer
from tech_three.utils.mixins import SerializerClassMixin, ContextMixin


class LoginView(GenericAPIView):
    """Login with phone and password"""
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get_response(self, token, phone):
        response = Response(
            {
                'message': 'Logged in Successfully',
                'token': token,
                'phone': phone
            },
            status=status.HTTP_200_OK
        )

        return response

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.get_response(serializer.validated_data.get('token'), serializer.validated_data.get('phone'))


class RoleViewSet(ReadOnlyModelViewSet):
    queryset = Role.objects.filter(mode='A')
    serializer_class = RoleSerializer
    permission_classes = (IsAdminUser,)
    search_fields = ['name', ]


class UserViewSet(SerializerClassMixin, ContextMixin, ModelViewSet):
    queryset = User.objects.all().order_by('first_name', 'last_name')
    serializer_class = UserSerializer
    serializer_action_classes = {
        'change_password': ChangePasswordSerializer
    }
    permission_classes = (IsAuthenticated,)
    search_fields = ['first_name', 'last_name', 'phone']

    @action(detail=True, methods=['put'], url_path='change-password', url_name='change-password')
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'message': _('Password changed successfully.')})

    def destroy(self, request, *args, **kwargs):
        # TODO: Soft delete is implemented. need to check for delete the record.
        instance = self.get_object()

        if instance == request.user:
            return Response({'error': 'You may not delete your own account.'}, status=status.HTTP_400_BAD_REQUEST)

        instance.mode = Mode.DEACTIVATED
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
