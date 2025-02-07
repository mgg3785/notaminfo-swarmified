from rest_framework import viewsets, status
from .models import Notams, ParsedNotams
from . import serializers
from .pagination import NotamsPagination
from rest_framework.response import Response


class NotamsViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = NotamsPagination
    requested_parsed = 'false'
    queryparams  = {'parsed':('true','false',None),'coordinates':('true','false',None)} # param : (valid values)


    def _get_requested_queryparams(self,queryparams : list | tuple = queryparams.keys()):
        requested_queryparams = dict()
        for queryparam in queryparams:
            queryparam_value = self.request.query_params.get(queryparam)
            if isinstance(queryparam_value, str):
                queryparam_value = queryparam_value.lower()
                requested_queryparams[queryparam] = queryparam_value
            else :
                requested_queryparams[queryparam] = 'false'
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
        notams_queryset = Notams.objects.all()
        match (requested_parsed,requested_coordinates):
            case 'true','false':
                notams_queryset = ParsedNotams.objects.all().order_by('notam')
            case 'true','true':
                notams_queryset = ParsedNotams.objects.select_related('notam').prefetch_related('notam__coordinates').order_by('notam')
            case 'false','true':
                notams_queryset = Notams.objects.prefetch_related('coordinates')

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

        


class ParsedNotamsViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ParsedNotamsSerializer
    def get_queryset(self):
        print(self.kwargs)
        notam_pk = self.kwargs.get('notam_pk')
        if notam_pk:
            return ParsedNotams.objects.filter(notam_id=notam_pk)
        return ParsedNotams.objects.all()
        

