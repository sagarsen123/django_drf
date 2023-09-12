from rest_framework import serializers
from .models import *

# model Serializers = when you want to use the functionality with model
# serilizers.Serialzer = when you want to customize the serializer completely

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()










class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']
    

class PeopleSerializer(serializers.ModelSerializer):

    color = ColorSerializer()
    color_info = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = '__all__'
        # exclude =  ['name', 'age']
        # specifying level to show on output
        # depth = 1

    # Can add a method to add field from instead of the model
    def get_color_info(self, obj):
        # grabbing data from other tables
        color_obj = Color.objects.get(id = obj.color.id)
        return {'color_name': color_obj.color_name, 'hex_code' : '#000'}

    # VALIDATING THE DATA THROUGH SERIALIZER
    def validate(self, data):

        special_charters = "!@#$%^&*()_+?-=<>/"
        if any(C in special_charters for C in data['name']):
            raise serializers.ValidationError('name cannot contain special characters')

        if data['age'] < 18:
            raise serializers.ValidationError('Age should be greater than 18')
        return data