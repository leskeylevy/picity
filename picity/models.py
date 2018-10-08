from django.db import models
from django.contrib.auth.models import User
import datetime as dt


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    dp = models.ImageField(upload_to='images')
    bio = models.CharField(max_length=100)

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profile(cls, id):
        profile = cls.objects.all()
        return profile

    @classmethod
    def update_profile(cls, id, update):
        profile_update = cls.objects.filter(id=id).update(profile=update)
        return profile_update

    def __str__(self):
        return self.user.username


class Image(models.Model):
    user = models.ForeignKey(User)
    image = models.ImageField(upload_to='posts')
    caption = models.CharField(max_length=140)
    profile = models.ForeignKey(Profile, null=True)
    posted_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['posted_time']

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    @classmethod
    def update_image(cls, id, update):
        update_image = cls.objects.filter(id=id).update(target=update)
        return update_image

    @classmethod
    def get_all(cls):
        images = cls.objects.order_by('posted_time')
        return images

    @classmethod
    def get_image(cls, id):
        image = cls.objects.get(id=id)
        return image


class Comments(models.Model):
    user = models.ForeignKey(User)
    image = models.ForeignKey(Image)
    comment = models.CharField(max_length=200)

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

    @classmethod
    def update_comment(cls, id, update):
        comment_update = cls.objects.filter(id=id).update(comment=update)
        return comment_update

    def __str__(self):
        return self.comment
