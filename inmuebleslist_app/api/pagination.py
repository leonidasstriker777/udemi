# Libraries
from rest_framework.pagination import (PageNumberPagination, LimitOffsetPagination, )


# Class EdificacionPagination
class EdificacionPagination(PageNumberPagination):
    page_size = 2
    # Renombrar page -> p
    page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 10
    last_page_strings = 'end'

# Offset y paginacion
class EdificacionLOPagination(LimitOffsetPagination):
    default_limit = 1