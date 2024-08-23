from django.urls import path

from post.views import PostViewset, CommentViewset

urlpatterns = [
    path(
        "post/",
        PostViewset.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="post",
    ),
    path(
        "post/<int:pk>/",
        PostViewset.as_view(
            {
                "patch": "update",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "user/<int:user_id>/post/<int:post_id>",
        CommentViewset.as_view(
            {
                "get":"list",
                "post":"create"
            }
        )
    ),
]
