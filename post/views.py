from django.shortcuts import render
from post.models import Post
from rest_framework import viewsets
from post.Serializer import PSerializer
from rest_framework.response import Response
from rest_framework import status
from utils.pagination import Pagination
from rest_framework.filters import SearchFilter


# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(deleted=0).order_by("-id")
    serializer_class = PSerializer
    pagination_class = Pagination
    filter_backends = [SearchFilter]
    
    search_fields = [
        "author__id",
        "title",
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