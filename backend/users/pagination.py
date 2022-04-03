from rest_framework import pagination


class CustomPagination(pagination.LimitOffsetPagination):
    # default_limit = 1
    pass
