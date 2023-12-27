from rest_framework.decorators        import api_view
from rest_framework.response          import Response
from user_app.api.serializers         import RegistrationSerializer
from rest_framework.authtoken.models  import Token
from user_app                         import models
from rest_framework                   import status


# Cerrar Sesion
@api_view(['POST'], )
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
        
        
# Registrar nuevo User
@api_view(['POST'], )
def resgistration_view(request):
    if request.method == 'POST':
        # Obtiene datos del Cliente, en Json
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        
        # Valida el serializer Creado. Si es unico y comparacion de passwords
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'El registro del usuario fue exitoso'
            data['username'] = account.username
            data['email'] = account.email
            # Retorna una instacia en Base64
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data=serializer.errors
            
        return Response(data)









