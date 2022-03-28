from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.LimitOffsetPagination):
    default_limit = 1