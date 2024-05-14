from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError

# Serializer for retrieving user data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('user_id', 'username', 'email', 'password', 'name', 'phone' )  

# Serializer for creating new users
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': True}
        }
    
    # Customize representation of user data    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = representation['name'].capitalize()
        representation.pop('last_login', None)
        return representation
    
    # Validate user data
    def validate(self, data):
        email = data.get('email', '').strip().lower()
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except DjangoValidationError:
            raise serializers.ValidationError({'email': ['Invalid email format.']})

        password = data.get('password')
        validate_password(password)

        phone = data.get('phone')
        if len(str(phone)) != 10:
            raise serializers.ValidationError({'phone': ['Phone number must be 10 digits long.']})

        name = data.get('name')
        if not name.isalpha():
            raise serializers.ValidationError({'name': ['Name must only contain alphabetic characters.']})
        
        return data
    
    # Create a new user with validated data
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
        