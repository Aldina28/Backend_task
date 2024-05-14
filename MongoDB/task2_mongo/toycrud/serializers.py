from rest_framework import serializers
from toycrud.models import Toy
from django.core.validators import RegexValidator, MinValueValidator

#Serializer for the Toy model.
class ToyModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[RegexValidator(regex='^[a-zA-Z\s]*$', message='Name must only contain alphabetic characters', code='invalid_name')])
    model = serializers.CharField(max_length=10,)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])  

    class Meta:
        model = Toy
        fields = "__all__"