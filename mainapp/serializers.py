from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

from rest_framework import serializers

from .models import User, Criterion, Indicator, Document


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'date_joined', 'last_login']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'email': {
                'required': True
            },
            'password': {
                'write_only': True,
                'required': True
            },
            'date_joined': {
                'read_only': True
            },
            'last_login': {
                'read_only': True
            },

        }


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'designation', 'department', 'institution']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'email': {
                'required': True
            }
        }


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("password", ),
        style={"input_type": "password"},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                msg = _("Unable to Login with the credentials provided")
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _("Must include email and password.")
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs


class CriterionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criterion
        fields = ['id', 'number', 'name', 'description']


# class ListCriterionSerializer(serializers.Serializer):
#     id = serializers.UUIDField()

class IndicatorSerializer(serializers.ModelSerializer):
    # criterion = ListCriterionSerializer()

    class Meta:
        model = Indicator
        fields = [ 'id', 'name', 'description']



class DocumentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    indicator = IndicatorSerializer()

    class Meta:
        model = Document
        fields = ['user', 'indicator', 'content']


class ListDocumentSerializer(serializers.Serializer):
    id = serializers.UUIDField()


# class ProfileSerializer(serializers.ModelSerializer):
#     user = serializers.EmailField(label=_("Email"))
#
#     class Meta:
#         model = Profile
#         fields = ['user', 'full_name', 'contact', 'college_name', 'year_of_study']
#         extra_kwargs = {
#             "user": {
#                 "required": True
#             }
#         }
