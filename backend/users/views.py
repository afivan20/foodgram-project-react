from django import views
from users.models import User, Follow
from users.serializers import UserSerializer, UserDetailSerializer, SubscriptionsSerializer
from users.serializers import FollowSerializer
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserDetailSerializer

#     @action(
#         detail=False,
#         methods=('get',),
#         permission_classes=(IsAuthenticated,)
#     )
#     def mee(self, request):
#         serializer = UserSerializer(request.user,
#                                     data=request.data,
#                                     partial=True)

#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class Subsribe(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailSerializer

    def post(self, request, pk):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if author == user:
            return Response({
                    'errors': 'Вы не можете подписываться на самого себя'
                }, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user, author=author).exists():
            return Response({'errors': 'Вы уже подписаны на данного пользователя'},
                            status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.get_or_create(user=user, author=author)
        follow=User.objects.filter(username=author).first()
        serializer = FollowSerializer(
                follow, context={'request': request}
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=('delete',), permission_classes=(IsAuthenticated,))
    def delete(self, request, pk):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if user == author:
            return Response({
                'errors': 'Вы не можете отписываться от самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.filter(user=user, author=author)
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'Вы уже отписались'
        }, status=status.HTTP_400_BAD_REQUEST)




class Subscriptions(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        data = Follow.objects.filter(user=user)
        #pages = self.paginate_queryset(data)
        serializer = SubscriptionsSerializer(
            data,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)  # self.get_paginated_response(serializer.data) 


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)
