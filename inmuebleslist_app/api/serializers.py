from rest_framework import serializers
from inmuebleslist_app.models import Inmueble


class InmuebleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    direccion = serializers.CharField()
    pais = serializers.CharField()
    description = serializers.CharField()
    imagen = serializers.CharField()
    active = serializers.BooleanField()
    
    def create(self, validate_data):
        return Inmueble.objects.create(**validate_data)
    
    def update(self, instance, validated_data):
        instance.direccion = validated_data.get('direccion', instance.direccion)
        instance.pais = validated_data.get('pais', instance.pais)
        instance.description = validated_data.get('description', instance.description)
        instance.imagen = validated_data.get('imagen', instance.imagen)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance