
from platform import platform
from django.forms import ValidationError
from rest_framework import serializers

from watchlist.models import WatchList,StreamPlatform,Review

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        exclude = ('watchlist',)
      

class WatchListSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source='platform.name')
    
    class Meta:
        model = WatchList
        fields = "__all__"
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist= WatchListSerializer(many=True, read_only= True)
    
    
    class Meta:
        model = StreamPlatform
        fields= "__all__"        
        


        
