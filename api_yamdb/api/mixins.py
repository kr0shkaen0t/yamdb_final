from rest_framework import filters, mixins, viewsets

from .permissions import IsAdminOrReadOnly


class CreateDestroyListViewSet(mixins.DestroyModelMixin,
                               mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
