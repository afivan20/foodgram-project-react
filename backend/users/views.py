from users.models import User, Follow
from users.serializers import UserSerializer, UserDetailSerializer
from recipes.serializers import FollowSerializer
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = FollowSerializer

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = UserSerializer(request.user,
                                    data=request.data,
                                    partial=True)

        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, permission_classes=[IsAuthenticated], methods=('post',))
    def subsribe(request):
        id = 3  # подписка захардкодена
        user = request.user
        author = get_object_or_404(User, id=id)
        if author == user:
            return Response({
                    'errors': 'Вы не можете подписываться на самого себя'
                }, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user, author=author).exists():
            return Response({'errors': 'Вы уже подписаны на данного пользователя'},
                            status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.get_or_create(user=user, author=author)
        serializer = FollowSerializer(
                follow, context={'request': request}
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)
