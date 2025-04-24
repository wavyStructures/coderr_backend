from rest_framework.pagination import PageNumberPagination

class OfferPagination(PageNumberPagination): 
    page_size = 10
    page_size_query_param = "page"
    
    