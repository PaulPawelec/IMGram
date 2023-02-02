from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # title = models.CharField(max_length=255)
    image_post = models.ImageField(null=False, blank=False, upload_to="images/")
    description = models.TextField()
    publication_date = models.DateField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name='post_likes')

    # date = models.DateField(auto_now_add=True)
    # like = models.ManyToManyField(User, related_name='posts')

    def __str__(self):
        return str(self.author) + self.description

    def get_absolute_url(self):
        return reverse('post_details', args=(str(self.id)))

    def likes_count(self):
        return self.like.count()


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to="images/avatars/")
    biography = models.TextField()
    followers = models.ManyToManyField(User, related_name='profile_followers')
    follows = models.ManyToManyField(User, related_name='profile_follows')

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        # return reverse('profile_details', args=(str(self.id)))
        return reverse('profile_details', kwargs={'pk': self.pk})

    def followers_count(self):
        return self.followers.count()

    def follows_count(self):
        return self.follows.count()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors')
    date_add = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return str(self.author) + ' ' + str(self.date_add)



