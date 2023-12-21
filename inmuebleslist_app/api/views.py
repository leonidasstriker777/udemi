#from rest_framework.decorators        import api_view
from rest_framework.views              import APIView
from rest_framework.response           import Response
from rest_framework                    import status  
from inmuebleslist_app.models          import (Edificacion, Empresa, Comentario, )
from inmuebleslist_app.api.serializers import (EdificacionSerializer, EmpresaSerializer, ComentarioSerializer, )
from rest_framework                    import (generics, mixins, )
from rest_framework                    import viewsets
from django.shortcuts                  import get_object_or_404
from rest_framework.exceptions         import ValidationError
from rest_framework.permissions        import IsAuthenticated
from inmuebleslist_app.api.permissions import (AdminOrReadOnly, ComentarioUserOrReadOnly, )



###############################
# VISTAS GENERICAS MODIFICADA #
###############################
class ComentarioCreate(generics.CreateAPIView):
    serializer_class = ComentarioSerializer
    
    def get_queryset(self):
        return Comentario.objects.all()
    
    # Reemplaza el perform_create por defecto.
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        inmueble = Edificacion.objects.get(pk=pk)
        
        user = self.request.user
        comentario_queryset = Comentario.objects.filter(edificacion=inmueble, comentario_user=user)
        if comentario_queryset.exists():
            raise ValidationError('El usuario ya escribio un comentario para este inmueble')

        if inmueble.number_calificacion == 0:
            inmueble.avg_calificacion = serializer.validated_data['calificacion']
        else:
            inmueble.avg_calificacion = (serializer.validated_data['calificacion'] + inmueble.avg_calificacion)/2
            
        inmueble.number_calificacion = inmueble.number_calificacion + 1
        
        inmueble.save()
        
        serializer.save(edificacion=inmueble, comentario_user=user)



class ComentarioList(generics.ListCreateAPIView):
    #queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    
    permission_classes = [IsAuthenticated]
    
    # Reemplaza el query por defecto.
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comentario.objects.filter(edificacion=pk)
    
    
class ComentarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer        
    
    permission_classes = [ComentarioUserOrReadOnly]



######################################################
# TRABAJAMOS CON ROUTES EN LAS URLS Y VIEWSET MODELS #
######################################################
# Solo mantenimiento genericos no para logica complejas
class EmpresaVS(viewsets.ModelViewSet):
    
    #permission_classes = [IsAuthenticated]
    permission_classes = [AdminOrReadOnly] 
        
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


######################################
# TRABAJAMOS CON ROUTES EN LAS URLS  #
######################################
# class EmpresaVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Empresa.objects.all()
#         serializer = EmpresaSerializer(queryset, many=True)
#         return Response(serializer.data)         
    
#     def retrieve(self, request, pk=None):
#         queryset = Empresa.objects.all()
#         edificacionlist = get_object_or_404(queryset, pk=pk)
#         serializer = EmpresaSerializer(edificacionlist)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = EmpresaSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
#     def update(self, request, pk):
#         try:
#             empresa = Empresa.objects.get(pk=pk)
#         except Empresa.DoesNotExist:
#             return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = EmpresaSerializer(empresa, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def destroy(self, request, pk):
#         try:
#             empresa = Empresa.objects.get(pk=pk)
#         except Empresa.DoesNotExist:
#             return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
#         empresa.delete()
#         return Response({'destroy': 'Registro eliminado con exito'}, status=status.HTTP_204_NO_CONTENT)
        
        
#################################
# VISTAS NORMALES CON API VIEW  #
#################################
class EmpresaAV(APIView):
    
    def get(self, request):
        empresas = Empresa.objects.all()
        # Aqui serializo el objeto empresa que deseo obtener desde el Servidor.
        serializer = EmpresaSerializer(empresas, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        # Aqui serializo el objeto empresa que recibo desde el Servidor, para mostrar al Cliente.
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmpresaDetalleAV(APIView):
    
    def get(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except empresa.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmpresaSerializer(empresa, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except empresa.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmpresaSerializer(empresa, data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except empresa.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        empresa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EdificacionAV(APIView):
    
    def get(self, request):
        inmuebles = Edificacion.objects.all()
        serializer = EdificacionSerializer(inmuebles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EdificacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    
class EdificacionDetalleAV(APIView):
    
    def get(self, request, pk):
        try:
            inmueble = Edificacion.objects.get(pk=pk)
        except Edificacion.DoesNotExist:
            return Response({'error': 'Inmueble no encontrado'}, status=status.HTTP_404_NOT_FOUND)            

        serializer = EdificacionSerializer(inmueble)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            inmueble = Edificacion.objects.get(pk=pk)
        except Edificacion.DoesNotExist:
            return Response({'error': 'Inmueble no encontrado'}, status=status.HTTP_404_NOT_FOUND)            

        serializer = EdificacionSerializer(inmueble, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        try:
            inmueble = Edificacion.objects.get(pk=pk)
        except Edificacion.DoesNotExist:
            return Response({'Error': 'El inmueble no existe'}, status = status.HTTP_404_NOT_FOUND)
        inmueble.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


####################
# VISTAS GENERICAS #
####################
# class ComentarioList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Comentario.objects.all()
#     serializer_class = ComentarioSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ComentarioDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Comentario.objects.all()
#     serializer_class = ComentarioSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)