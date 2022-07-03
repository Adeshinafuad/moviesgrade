from django.urls import path, include
from rest_framework.routers import DefaultRouter




# from .views import movie_list, movie_details
from .views import (ReviewDetail, StreamPlatformVS, WatchListAVI,
                    WatchListDetailAV,  StreamPlatformListAV,
                    StreamPlatformDetailAV,ReviewList, ReviewCreate, UserReviewSearch, WatchListView)

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path("list/", WatchListAVI.as_view() , name="movie-list" ),
    path("<int:pk>/", WatchListDetailAV.as_view(), name="movie-detail" ),
    path("list2/", WatchListView.as_view() , name="watch-list" ),
    
    
    path('', include(router.urls)),
    # path("stream/", StreamPlatformListAV.as_view(), name="stream"),
    # path("stream/<int:pk>", StreamPlatformDetailAV.as_view(), name="streamplatform-detail"),
    # path("review", ReviewList.as_view(), name="review-list"),
    # path("review/<int:pk>", ReviewDetail.as_view(), name="review-detail"),
    path("<int:pk>/review-create/", ReviewCreate.as_view(), name="review-create"),
    path("<int:pk>/reviews/", ReviewList.as_view(), name="review-list"),
    path("review/<int:pk>/", ReviewDetail.as_view(), name="review-detail"),
    path("reviews/", UserReviewSearch.as_view(), name='user-review-search' )
    
]
