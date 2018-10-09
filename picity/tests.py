from django.test import TestCase
from django.contrib.auth.models import User
from .models import Image, Profile, Comments


# Create your tests here.


class UserTest(TestCase):
    def setUp(self):
        self.user = User(username='koko', first_name='sobo', last_name='moto', email='ksm@gmail.com')

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_data(self):
        self.assertTrue(self.user.username, "koko")
        self.assertTrue(self.user.first_name, "sobo")
        self.assertTrue(self.user.last_name, 'moto')
        self.assertTrue(self.user.email, 'ksm@gmail.com')

    def test_save(self):
        self.user.save()
        users = User.objects.all()
        self.assertTrue(len(users) > 0)

    def test_delete(self):
        user = User.objects.filter(id=1)
        user.delete()
        users = User.objects.all()
        self.assertTrue(len(users) == 0)


class ProfileTest(TestCase):
    def setUp(self):
        self.new_user = User(username='aa', first_name='a', last_name='a', email='a@gmail.com')
        self.new_user.save()
        self.new_profile = Profile(user=self.new_user, bio='wueh')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile, Profile))

    def test_data(self):
        self.assertTrue(self.new_profile.bio, "wuehh")
        self.assertTrue(self.new_profile.user, self.new_user)

    def test_save(self):
        self.new_profile.save()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)

    def test_delete(self):
        profile = Profile.objects.filter(id=1)
        profile.delete()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) == 0)

    def test_edit_profile(self):
        self.new_profile.save()
        self.update_profile = Profile.objects.filter(bio='wueh').update(bio='aaabbbcccddd')
        self.updated_profile = Profile.objects.get(bio='aaabbbcccddd')
        self.assertTrue(self.updated_profile.bio, 'aaabbbcccddd')


class imagesTest(TestCase):
    def setUp(self):
        self.user = User(username='dk', first_name='d', last_name='k', email='dk@gmail.com')
        self.user.save()
        self.new_profile = Profile(user=self.user, bio='wueh')
        self.new_profile.save()
        self.new_post = Image(user=self.user, caption="eating", profile=self.new_profile)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post, Image))

    def test_data(self):
        self.assertTrue(self.new_post.caption, "eating")

    def test_save(self):
        self.new_post.save()
        posts = Image.objects.all()
        self.assertTrue(len(posts) > 0)

    def test_delete(self):
        post = Image.objects.filter(id=1)
        post.delete()
        posts = Image.objects.all()
        self.assertTrue(len(posts) == 0)

    def test_update_post(self):
        self.new_post.save()
        self.update_post = Image.objects.filter(caption='eating').update(caption='aaabbbcccddd')
        self.updated_post = Image.objects.get(caption='aaabbbcccddd')
        self.assertTrue(self.updated_post.caption, 'aaabbbcccddd')


class CommentTest(TestCase):
    def setUp(self):
        self.new_user = User(username='aa', first_name='a', last_name='a', email='a@gmail.com')
        self.new_user.save()
        self.new_profile = Profile(user=self.new_user, bio='wueh')
        self.new_profile.save()
        self.new_post = Image(user=self.new_user, caption="eating", profile=self.new_profile)
        self.new_post.save()
        self.comment = Comments(user=self.new_user, image=self.new_post, comment='good')

    def test_instance(self):
        self.assertTrue(isinstance(self.comment, Comments))

    def test_data(self):
        self.assertTrue(self.comment.comment, "good")

    def test_comments(self):
        self.comment.save()
        comments = Comments.objects.all()
        self.assertTrue(len(comments) > 0)
