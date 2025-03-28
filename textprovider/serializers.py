from rest_framework import serializers
from .models import Notams, ParsedNotams, Coordinates

class CoordniatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ['latitude','longitude']

class NotamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notams
        fields = ['id','notam_text']

class NotamsIncludeCoordinatesSerializer(NotamsSerializer):
    coordinates = CoordniatesSerializer(many=True,read_only=True)
    class Meta(NotamsSerializer.Meta):
        fields = NotamsSerializer.Meta.fields + ['coordinates']
    

class ParsedNotamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParsedNotams
        fields = ['notam','identifier','sec_q','sec_a','sec_b','sec_c','sec_d','sec_e','sec_f','created','source']

class ParsedNotamsIncludeCoordinatesSerializer(ParsedNotamsSerializer):
    coordinates = CoordniatesSerializer(source='notam.coordinates',many=True,read_only=True)
    class Meta(ParsedNotamsSerializer.Meta):
        fields = ParsedNotamsSerializer.Meta.fields + ['coordinates']

class QueryParamsSerializer(serializers.Serializer):
    choices = (('true', 'true'), ('false', 'false'))

    parsed = serializers.ChoiceField(choices=choices, required=False)
    coordinates = serializers.ChoiceField(choices=choices, required=False)
    search = serializers.CharField(allow_null=True, required=False)
    