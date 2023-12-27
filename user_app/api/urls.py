from django.urls                    import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views             import (resgistration_view, logout_view, )
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, )


urlpatterns = [
    
    # GENERAR EL LOGIN
    path('login/', obtain_auth_token, name='login'),
    # REGISTRAR USER
    path('register/', resgistration_view, name='register'),
    # LOGIUT USER
    path('logout/', logout_view, name='logout'),
    
    
    # LOGIUT USER
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # LOGIUT USER
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    

    
]