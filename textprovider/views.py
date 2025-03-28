from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from django_filters.rest_framework import DjangoFilterBackend

from textprovider.filters import NotamsFilter
from . import serializers
from .models import Notams, ParsedNotams
from .pagination import NotamsPagination


class NotamsViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = NotamsPagination
    permission_classes = [HasAPIKey]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NotamsFilter
    requested_parsed = 'false'

    def _validate_queryparams(self, requested_queryparams : dict):
        serializer = serializers.QueryParamsSerializer(data=self.request.query_params)
        validation_result = serializer.is_valid()
        if validation_result:
            validation_error = False
        else:
            validation_error = Response({'error': f"Invalid value."}, status=status.HTTP_400_BAD_REQUEST)
        return validation_error


    def retrieve(self, request, *args, **kwargs):
        validation_error = self._validate_queryparams(self.request.query_params)
        if validation_error:
            return validation_error
    
        if self.request.query_params.get('parsed') == 'true':
            notam_pk = self.kwargs.get('pk')
            queryset = self.get_queryset()         
            instance = get_object_or_404(queryset,notam=notam_pk)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
   
        return super().retrieve(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        validation_error = self._validate_queryparams(self.request.query_params)
        if validation_error:
            return validation_error
        return super().list(request, *args, **kwargs)
        
    def get_queryset(self):
        requested_parsed = self.request.query_params.get('parsed','false')
        requested_coordinates =  self.request.query_params.get('coordinates','false')
        match (requested_parsed,requested_coordinates):
            case 'true','false':
                notams_queryset = ParsedNotams.objects.select_related('notam').order_by('notam__id')
            case 'true','true':
                notams_queryset = ParsedNotams.objects.select_related('notam').prefetch_related('notam__coordinates').order_by('notam__id')
            case 'false','true':
                notams_queryset = Notams.objects.prefetch_related('coordinates').order_by('id')
            case _:    
                notams_queryset = Notams.objects.order_by('id')

        return notams_queryset
    
    def get_serializer_class(self):
        requested_parsed = self.request.query_params.get('parsed','false')
        requested_coordinates =  self.request.query_params.get('coordinates','false')
        notams_serializer = serializers.NotamsSerializer
        match (requested_parsed,requested_coordinates):
            case 'true','false':
                notams_serializer = serializers.ParsedNotamsSerializer
            case 'true','true':
                notams_serializer = serializers.ParsedNotamsIncludeCoordinatesSerializer
            case 'false','true':
                notams_serializer = serializers.NotamsIncludeCoordinatesSerializer

        return notams_serializer

        

        

