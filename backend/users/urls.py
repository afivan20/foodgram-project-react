from django.urls import include, path
from users.views import UserDetail


urlpatterns = [
    path('users/<int:pk>/', UserDetail.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
