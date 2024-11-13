from django_filters import FilterSet
from .models import *


class BoardFilter(FilterSet):
    class Meta:
        model = Advertisement
        fields = {
            'category': ['exact'],
        }


class MyBoardFilter(FilterSet):
    class Meta:
        model = Advertisement
        fields = {
            'title': ['icontains'],
        }
