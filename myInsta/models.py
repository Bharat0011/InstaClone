from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    curr_user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.TextField(null=True)
    user_bio = models.CharField(max_length=500,null=True)
    
    def __str__(self):
        return self.curr_user.first_name

class Post(models.Model):
    curr_user = models.ForeignKey(User,on_delete=models.CASCADE)
    curr_profile = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    post_image = models.TextField()
    post_caption = models.CharField(max_length=500)
    DateandTime = models.DateTimeField(("DateTime"),auto_now_add=datetime.datetime.now(),null=True)
    post_likes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-DateandTime',]

    def __str__(self):
        return self.curr_user.first_name

class Likes(models.Model):
    curr_user = models.ManyToManyField(User,related_name="User")
    post = models.OneToOneField(Post,on_delete=models.CASCADE)
    
    @classmethod
    def user_liked(cls,post,liking_user):
        obj,create = cls.objects.get_or_create(post=post)
        obj.curr_user.add(liking_user)
        obj.post.post_likes = obj.post.post_likes + 1
        obj.post.save()

    @classmethod
    def user_disliked(cls ,post, disliking_user):
        obj,create = cls.objects.get_or_create(post=post)
        obj.curr_user.remove(disliking_user)
        obj.post.post_likes = obj.post.post_likes - 1
        obj.post.save()

    def __str__(self):
        return (str(self.post)+"\t"+ str(self.post.DateandTime))

class Follow(models.Model):
    curr_user = models.OneToOneField(User,on_delete=models.CASCADE)
    followed = models.ManyToManyField(User,related_name="followed")

    @classmethod
    def follow(cls,curr_user,another_user):
        obj,create = cls.objects.get_or_create(curr_user=curr_user)
        obj.followed.add(another_user)
        

    @classmethod
    def unfollow(cls,curr_user,another_user):
        obj,create = cls.objects.get_or_create(curr_user=curr_user)
        obj.followed.remove(another_user)

    def __str__(self):
        return self.curr_user.first_name
    

class Comments(models.Model):
    curr_user = models.ForeignKey(User,on_delete=models.CASCADE)
    curr_post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    curr_profile_pic = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='com_profile_pic',null=True)
    comment = models.TextField(null=True)

    def __str__(self):
        return (str(self.curr_post)+"\t"+ str(self.curr_post.DateandTime))    

