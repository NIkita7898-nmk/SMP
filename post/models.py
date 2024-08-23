from django.db import models

from user.models import CustomUser


# Create your models here.
class Post(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    caption = models.CharField(max_length=1000, null=True)
    number_of_likes = models.IntegerField(null=True)
    images = models.ImageField(upload_to="media/", null=False)


class Comments(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_id")
    comment = models.CharField(max_length=500)


