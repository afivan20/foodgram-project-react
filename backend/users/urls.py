from django.urls import include, path
from users.views import UserViewSet, Subsribe

app_name = 'users'

urlpatterns = [
   # path('users/<int:pk>/', UserDetail.as_view()),
    path('users/<int:pk>/subscribe/', Subsribe.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
