from django.shortcuts import render
from user.models import User
from rest_framework import viewsets
from user.Serializer import USerializer
from rest_framework.response import Response
from rest_framework import status
from utils.pagination import Pagination
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from datetime import datetime


# Create your views here.


class UserFilter(filters.FilterSet):
    created_at = filters.CharFilter(method='filter_date')
    updated_at = filters.CharFilter(method='filter_date')
    last_login = filters.CharFilter(method='filter_date')

    class Meta:
        model = User
        fields = ['created_at', 'updated_at', 'last_login']

    def filter_date(self, queryset, name, value):
        # Define possible date formats
        date_formats = [
            '%Y-%m-%d',             # 2024-11-10
            '%d-%m-%Y',             # 10-11-2024
            '%m/%d/%Y',             # 11/10/2024
            '%Y/%m/%d',             # 2024/11/10
            '%Y-%m-%dT%H:%M:%S%z',  # 2024-11-10T15:30:00Z
            '%Y-%m-%dT%H:%M:%S.%f%z', # 2024-11-10T15:30:00.000000Z
            '%Y-%m-%dT%H:%M:%S',    # 2024-11-10T15:30:00
            '%Y-%m-%d %H:%M:%S',    # 2024-11-10 15:30:00
            '%Y-%m-%d %H:%M:%S.%f', # 2024-11-10 15:30:00.000000
            '%m/%d/%Y %H:%M:%S',    # 11/10/2024 15:30:00
            '%d-%m-%Y %H:%M:%S' 
        ]
        # Try parsing the date with each format
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(value, date_format)
                return queryset.filter(**{name: parsed_date})
            except ValueError:
                continue
        return queryset.none()  # If no format matches, return an empty queryset



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(deleted=0).order_by("-id")
    serializer_class = USerializer
    pagination_class = Pagination     
    filter_backends = [SearchFilter]
    
    
    search_fields = [
        "id",
        "username",
        "email",
        "created_at"
    ]
    
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None: 
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data) 
        serializer = self.serializer_class(queryset, many=True)
        return Response({'success': True, 'data': serializer.data})
    
   
    def create(self, request, *args, **kwargs):
        data=request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response({'success': True, 'data': serializer.data})
           
       
       
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': 'Data Successfully Updated!'}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = 1
        instance.save()
        return Response({'success': True, 'data': 'Data Deleted.'})