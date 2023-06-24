
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from .views import ArticleList , ArticleDetail ,RegisterUser , UserProfile

urlpatterns = [
    path('api/v1/register', RegisterUser.as_view(), name='register-user'),
    path('api/v1/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/get-profile' ,UserProfile.as_view() , name = 'get-user-profile' ),
    path('api/v1/articles', ArticleList.as_view(), name='article-list'),
    path('api/v1/articles/<int:pk>', ArticleDetail.as_view(), name='article-detail'),
    
]
