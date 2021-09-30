from django.contrib.auth import authenticate, password_validation
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User, Role, Mode, Country, State
from tech_three.utils.validators import PHONE_REGEX, NAME_REGEX


class LoginSerializer(serializers.Serializer):
    """Serializer for Login endpoint"""
    phone = serializers.CharField(label=_('Phone'), allow_blank=False, validators=[PHONE_REGEX])
    password = serializers.CharField(
        label=_('Password'),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        if phone and password:
            user = self.authenticate(phone=phone, password=password)

            if not user:
                raise serializers.ValidationError({'error': _('Unable to login with provided credentials.')},
                                                  code='authorization')

            if user.mode == Mode.DEACTIVATED:
                raise serializers.ValidationError(
                    {'error': _('User account is suspended. Contact your administrator.')}, code='authorization')

            token = RefreshToken.for_user(user)
            jwt_token = str(token.access_token)

            return {
                'phone': str(user.phone),
                'token': jwt_token
            }


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role details"""
    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'mode')


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country details"""
    class Meta:
        model = Country
        fields = ('id', 'name', )


class StateSerializer(serializers.ModelSerializer):
    """Serializer for State details"""

    class Meta:
        model = State
        fields = ('id', 'name', )

    def to_representation(self, instance):
        data = super(StateSerializer, self).to_representation(instance=instance)
        data['name'] = data['name'].title()
        return data


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User details"""
    first_name = serializers.CharField(label=_('First Name'), allow_blank=False, validators=[NAME_REGEX])
    last_name = serializers.CharField(label=_('Last Name'), allow_blank=False, validators=[NAME_REGEX])

    class Meta:
        model = User
        fields = ('id', 'phone', 'first_name', 'last_name', 'is_active', 'mode', 'address_line1', 'address_line2',
                  'city',  'postal_code', 'state', 'country', 'role')

    def update(self, instance, validated_data):
        instance.modified_by = self.context.get('request').user
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for password change endpoint.
    """
    current_password = serializers.CharField(label='Current Password', write_only=True,
                                             style={'input_type': 'password'})
    new_password = serializers.CharField(label='New Password', write_only=True, style={'input_type': 'password'})
    confirm_new_password = serializers.CharField(label='Confirm New Password', write_only=True,
                                                 style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('current_password', 'new_password', 'confirm_new_password')

    def validate_current_password(self, password):
        user = self.context.get('request').user
        if not user.check_password(password):
            raise serializers.ValidationError(_('Sorry, the current password which you have given is not matching'))

        return password

    def validate_new_password(self, password):
        try:
            password_validation.validate_password(password)
        except ValidationError as errors:
            raise serializers.ValidationError(errors)

        return password

    def validate(self, data):
        if data.get('new_password') != data.get('confirm_new_password'):
            raise serializers.ValidationError({'confirm_new_password': "Those passwords don't match."})

        try:
            password_validation.validate_password(data.get('confirm_new_password'))
        except ValidationError as errors:
            raise serializers.ValidationError({'confirm_new_password': errors})

        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['confirm_new_password'])
        instance.modified_by = instance
        instance.save()

        return instance
