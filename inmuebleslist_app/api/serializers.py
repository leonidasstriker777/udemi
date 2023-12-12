from rest_framework import serializers
from inmuebleslist_app.models import Edificacion, Empresa


class EdificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edificacion
        fields = "__all__"
        #fields = ['id', 'pais', 'imagen', 'active']
        #exclude = ['id']


class EmpresaSerializer(serializers.HyperlinkedModelSerializer):
    
    edificacionlist = EdificacionSerializer(many=True, read_only=True)
    #edificacionlist = serializers.StringRelatedField(many=True)
    #edificacionlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #edificacionlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='edificacion-detalle')
    
    class Meta:
        model = Empresa
        fields = "__all__"




        






    
    # def get_longitud_direccion(self, object):
    #     cantidad_caracteres = len(object.direccion)
    #     return cantidad_caracteres
        
        
    # def create(self, validate_data):
    #     return Inmueble.objects.create(**validate_data)
    

    
    # def validate(self, data):
    #     if data['direccion'] == data['pais']:
    #         raise serializers.ValidationError('La direccion y pais deben ser diferentes')
    #     else:
    #         return data
        
        
    # def validate_imagen(self, data):
    #     if len(data) < 2:
    #         raise serializers.ValidationError('La url de la imagen es muy corta')
    #     else:
    #         return data




# def column_longitud(value):
#     if len(value) < 2:
#         raise serializers.ValidationError('La longitud debe ser mayor a 2 caracteres')
    

# class InmuebleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     direccion = serializers.CharField(validators=[column_longitud])
#     pais = serializers.CharField(validators=[column_longitud])
#     description = serializers.CharField()
#     imagen = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validate_data):
#         return Inmueble.objects.create(**validate_data)
    
#     def update(self, instance, validated_data):
#         instance.direccion = validated_data.get('direccion', instance.direccion)
#         instance.pais = validated_data.get('pais', instance.pais)
#         instance.description = validated_data.get('description', instance.description)
#         instance.imagen = validated_data.get('imagen', instance.imagen)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate(self, data):
#         if data['direccion'] == data['pais']:
#             raise serializers.ValidationError('La direccion y pais deben ser diferentes')
#         else:
#             return data
        
#     def validate_imagen(self, data):
#         if len(data) < 2:
#             raise serializers.ValidationError('La url de la imagen es muy corta')
#         else:
#             return data