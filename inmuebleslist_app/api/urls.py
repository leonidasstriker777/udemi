#from inmuebleslist_app.api.views import inmueble_list, inmueble_detalle
from django.urls                  import path
from inmuebleslist_app.api.views  import (EdificacionAV, EdificacionDetalleAV, EmpresaAV,\
EmpresaDetalleAV, ComentarioList, ComentarioDetail)


urlpatterns = [
    
    #################################
    # VISTAS NORMALES CON API VIEW  #
    #################################
    path('list/', EdificacionAV.as_view(), name='edificacion'),
    path('<int:pk>', EdificacionDetalleAV.as_view(), name='edificacion-detail'),
    path('empresa/', EmpresaAV.as_view(), name='empresa'),
    path('empresa/<int:pk>', EmpresaDetalleAV.as_view(), name='empresa-detail'),
    
    
    ####################
    # VISTAS GENERICAS #
    ####################
    path('comentario/', ComentarioList.as_view(), name='comentario-list'),
    path('comentario/<int:pk>', ComentarioDetail.as_view(), name='comentario-detail'),
]