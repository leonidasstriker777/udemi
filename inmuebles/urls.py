from django.contrib  import admin
from django.urls     import path, include

urlpatterns = [
    
    # ADMINISTRADOR DEL PANEL
    path('admin/', admin.site.urls),

    # WEB APIS
    path('tienda/', include('inmuebleslist_app.api.urls'), ),
    
]
