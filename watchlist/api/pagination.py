from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 5
    # page_query_param = 'p'
    page_size_query_param = 'size'
    max_limit = 10
    
    
class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 5
    
class  WashListCpagination(CursorPagination):
    page_size =5
    ordering = 'created'