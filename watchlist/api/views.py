
import imp
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
#from rest_framework.decorators import api_view
from watchlist.models import StreamPlatform,  Review, WatchList
from .serializers import (ReviewSerializer, WatchListSerializer,
                          StreamPlatformSerializer)
from rest_framework import status, generics,mixins,viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrReadOnly, IsReviewerOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle,ScopedRateThrottle
from .throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import WatchListPagination,WatchListLOPagination,WashListCpagination

class UserReviewSearch(generics.ListAPIView):
    serializer_class = ReviewSerializer

    
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(reviewer__username=username)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        
        reviewer = self.request.user
        reviewer_queryset = Review.objects.filter(watchlist=watchlist,reviewer=reviewer)
        
        if reviewer_queryset.exists():
            raise ValidationError("You have already reviewed this movie")
        
        if watchlist.number_of_ratings == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'] )/2
        
        watchlist.number_of_ratings += 1
        watchlist.save()
        serializer.save(watchlist=watchlist, reviewer=reviewer)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reviewer__username', 'active']
    
    
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewerOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    

class WatchListView(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = [IsAdminOrReadOnly]

    pagination_class = WashListCpagination


class WatchListAVI(APIView, WashListCpagination):
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = WashListCpagination
    
    def get(self, request):
        movie=WatchList.objects.all()
        serializer = WatchListSerializer(movie, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class WatchListDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error':'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)



class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class= StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
    


        
class StreamPlatformListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        stream_platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(stream_platform, many = True, context={'request': request})
        return Response(serializer.data)   
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            stream_platform=StreamPlatform.objects.get(pk=pk)
            
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Stream platform not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(stream_platform, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        stream_platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(stream_platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        stream_platform = StreamPlatform.objects.get(pk=pk)
        stream_platform.delete()
        return Response(status =status.HTTP_404_NOT_FOUND)
        




