from django.urls import include, path
from users.views import UserDetail, UserViewSet

app_name = 'users'

urlpatterns = [
    path('users/<int:pk>/', UserDetail.as_view()),
    path('users/<int:pk>/subscribe/', UserViewSet.as_view(actions={'post': 'create'})),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
