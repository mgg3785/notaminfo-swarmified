from rest_framework import viewsets, status
from .models import Notams, ParsedNotams
from . import serializers
from .pagination import NotamsPagination
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from django.shortcuts import get_object_or_404


class NotamsViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = NotamsPagination
    permission_classes = [HasAPIKey]
    requested_parsed = 'false'
    
    # param : (valid values)
    queryparams  = {
        'parsed':('true','false'),
        'coordinates':('true','false')
                    } 
                    
    def _get_requested_queryparams(self, queryparams: list | tuple = None):
        if queryparams is None:
            queryparams = self.queryparams.keys()

        requested_queryparams = dict()
        for queryparam in queryparams:
            queryparam_value = self.request.query_params.get(queryparam,'').lower()
            requested_queryparams[queryparam] = queryparam_value if queryparam_value else 'false'
        return requested_queryparams

    def _validate_queryparams(self, requested_queryparams : dict):
        for validating_param in requested_queryparams.keys():
            valid_values = self.queryparams[validating_param]
            if requested_queryparams[validating_param] not in valid_values:
                return Response(
                    {'error': f"Invalid value, expected valid values : {valid_values}."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return None

    def retrieve(self, request, *args, **kwargs):
        queryparams_values = self._get_requested_queryparams()
        validation_error = self._validate_queryparams(queryparams_values)
        if validation_error:
            return validation_error
    
        if queryparams_values.get('parsed') == 'true':
            notam_pk = self.kwargs.get('pk')
            queryset = self.get_queryset()         
            instance = get_object_or_404(queryset,notam=notam_pk)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
   
        return super().retrieve(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryparams_values = self._get_requested_queryparams()
        validation_error = self._validate_queryparams(queryparams_values)
        if validation_error:
            return validation_error
        return super().list(request, *args, **kwargs)
        
    def get_queryset(self):
        queryparams_values = self._get_requested_queryparams()
        requested_parsed = queryparams_values['parsed']
        requested_coordinates =  queryparams_values['coordinates']
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
        queryparams_values = self._get_requested_queryparams()
        print(queryparams_values)
        requested_parsed = queryparams_values['parsed']
        requested_coordinates =  queryparams_values['coordinates']
        notams_serializer = serializers.NotamsSerializer
        match (requested_parsed,requested_coordinates):
            case 'true','false':
                notams_serializer = serializers.ParsedNotamsSerializer
            case 'true','true':
                notams_serializer = serializers.ParsedNotamsIncludeCoordinatesSerializer
            case 'false','true':
                notams_serializer = serializers.NotamsIncludeCoordinatesSerializer

        return notams_serializer

        

        

