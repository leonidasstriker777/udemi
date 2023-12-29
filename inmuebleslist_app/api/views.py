# Libraries
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
from inmuebleslist_app.api.permissions import (IsAdminOrReadOnly, IsComentarioUserOrReadOnly, )
from rest_framework.throttling         import (UserRateThrottle, AnonRateThrottle, ScopedRateThrottle, )
from inmuebleslist_app.api.throttling  import (ComentarioCreateThrottle, ComentarioListThrottle, )
from django_filters.rest_framework     import DjangoFilterBackend
from rest_framework                    import filters

# 1. Classes

# 1.1 Class UsuarioComentario
class UsuarioComentario(generics.ListAPIView):
    serializer_class = ComentarioSerializer
    # def get_queryset(self):
    #     # Parametro que envia el cliente
    #     username = self.kwargs['username']
    #     # Retorna todos los comentarios de un determinado usuario
    #     return Comentario.objects.filter(comentario_user__username=username)
    # Obtiene el valor directamente desde un parametro en la URL    
    def get_queryset(self):
        # Parametro capturado desde la url
        username = self.request.query_params.get('username', None)
        # Retorna todos los comentarios de un determinado usuario
        return Comentario.objects.filter(comentario_user__username=username)
    

# 1.2 Class ComentarioCreate
class ComentarioCreate(generics.CreateAPIView):
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ComentarioCreateThrottle]
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


# 1.3 Class ComentarioList
class ComentarioList(generics.ListCreateAPIView):
    #queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    #permission_classes = [IsAuthenticated]
    throttle_classes = [ComentarioListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comentario_user__username', 'active']
    #throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # Reemplaza el query por defecto.
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comentario.objects.filter(edificacion=pk)
    

# 1.4 Class ComentarioDetail
class ComentarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [IsComentarioUserOrReadOnly]
    # Posibilidad que un usuario anonimo y logueado verifiquen
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope   = 'comentario-detail'


# 1.5 Class EmpresaVS
class EmpresaVS(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminOrReadOnly]
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


# 1.6 Class EmpresaAV
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


# 1.7 Class EmpresaDetalleAV
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


# 1.8 Class EdificacionList
class EdificacionList(generics.ListAPIView):
    queryset = Edificacion.objects.all()
    serializer_class = EdificacionSerializer
    # Busqueda exacta
    #filter_backends = [DjangoFilterBackend]
    # Busqueda por coincidencias, y ordenamiento.
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    #filterset_fields = ['direccion', 'empresa__nombre']
    search_fields = ['direccion', 'empresa__nombre']


# 1.9 Class EdificacionAV
class EdificacionAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
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


# 1.10 Class EdificacionDetalleAV
class EdificacionDetalleAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
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