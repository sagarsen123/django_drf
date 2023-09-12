from rest_framework import serializers
from .models import Person

class PeopleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        # exclude =  ['name', 'age']
        fields = '__all__'