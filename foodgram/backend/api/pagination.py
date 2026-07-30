from rest_framework.pagination import PageNumberPagination

from recipes import constants


class VariablePageSizePagination(PageNumberPagination):
    """Пагинатор с настраиваемым количеством объектов."""

    page_size = constants.PAGE_SIZE_DEFAULT
    page_size_query_param = constants.PAGE_SIZE_QUERY_PARAM
