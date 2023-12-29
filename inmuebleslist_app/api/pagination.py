# Libraries
from rest_framework.pagination import PageNumberPagination


# Class EdificacionPagination
class EdificacionPagination(PageNumberPagination):
    page_size = 2
    # Renombrar page -> p
    page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 10
    last_page_strings = 'end'