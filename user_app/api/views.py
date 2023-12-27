from rest_framework.decorators import api_view
from rest_framework.response   import Response
from user_app.api.serializers  import RegistrationSerializer


# Registrar nuevo User
@api_view(['POST'], )
def resgistration_view(request):
    if request.method == 'POST':
        # Obtiene datos del Cliente, en Json
        serializer = RegistrationSerializer(data=request.data)
        # Valida el serializer Creado. Si es unico y comparacion de passwords
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)









