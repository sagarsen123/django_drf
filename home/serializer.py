from rest_framework import serializers
from .models import *

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']
    

class PeopleSerializer(serializers.ModelSerializer):

    color = ColorSerializer()

    class Meta:
        model = Person
        fields = '__all__'
        # exclude =  ['name', 'age']
        # specifying level to show on output
        # depth = 1

    # VALIDATING THE DATA THROUGH SERIALIZER
    def validate(self, data):

        special_charters = "!@#$%^&*()_+?-=<>/"
        if any(C in special_charters for C in data['name']):
            raise serializers.ValidationError('name cannot contain special characters')

        if data['age'] < 18:
            raise serializers.ValidationError('Age should be greater than 18')
        return data