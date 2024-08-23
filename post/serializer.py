from rest_framework import serializers

from post.models import Post, Comments


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ["comment"]


class PostSerializer(serializers.ModelSerializer):

    comment = serializers.SerializerMethodField("get_comment")
    user = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        post = Post.objects.create(
            caption=validated_data.get("caption", ""),
            user=user,
            images=validated_data.get("images"),
        )
        return post

    def get_comment(self, obj):
        comment = CommentSerializer(
            Comments.objects.filter(user=self.context["request"].user, post=obj),
            many=True,
            read_only=True,
        ).data
        return comment
