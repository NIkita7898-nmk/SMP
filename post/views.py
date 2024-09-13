from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from post.models import Post, Comments
from post.serializer import PostSerializer, CommentSerializer
from user.models import CustomUser
from utils.token import UserMixin


# Create your views here.
class PostViewset(UserMixin, viewsets.ModelViewSet):

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.get_user()
  
        return Post.objects.filter(user=user)

    def get_serializer_context(self):
        return {"request": self.request}

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Add custom logic here if needed
        if "caption" in request.data:
            caption = request.data["caption"]
            request.data["caption"] = f"Updated: {caption}"

        self.perform_update(serializer)

        return {"data": serializer.data}


class CommentViewset(UserMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.get_user()
        return Comments.objects.filter(user=user)

    def get_serializer_context(self):
        return {"request": self.request}

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():

            user_id = self.kwargs.get("user_id")
            user = CustomUser.objects.get(id=user_id)
            post_id = self.kwargs.get("post_id")
            post = Post.objects.filter(id=post_id, user=user_id).first()
            comment = request.data.get("comment")
            comment_obj = Comments.objects.create(user=user, post=post, comment=comment)
            comment_obj.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
