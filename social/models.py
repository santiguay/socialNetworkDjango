from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




# Class Profile: Represents the Profile model in the Django application.
class Profile(models.Model):
    # user: A OneToOneField establishing a one-to-one relationship with the built-in User model in Django.
    # Each profile is linked to a single user, and if a user is deleted, the associated profile will also be deleted (on_delete=models.CASCADE).
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # image: An ImageField used to store the profile image.
    # It has a default value of 'th.jpg', which will be used if no image is uploaded.
    image = models.ImageField(default='th.jpg')

    def __str__(self):
        # __str__: Method overridden to return a string representation of the profile.
        # It displays the username of the associated user.
        return f'Perfil de {self.user.username}'

    def following(self):
        # following: Method defined to retrieve the users followed by the current profile user.
        # It queries the Relationship model for all entries where the current profile's user is in the 'from_user' field.
        user_ids = Relationship.objects.filter(from_user=self.user).values_list('to_user_id', flat=True)
        # It returns a queryset of User objects that match the extracted user IDs.
        return User.objects.filter(id__in=user_ids)

    def followers(self):
        # followers: Method defined to retrieve the users following the current profile user.
        # It queries the Relationship model for all entries where the current profile's user is in the 'to_user' field.
        user_ids = Relationship.objects.filter(to_user=self.user).values_list('from_user_id', flat=True)
        # It returns a queryset of User objects that match the extracted user IDs.
        return User.objects.filter(id__in=user_ids)

# Class Post: Represents the Post model in the Django application.
class Post(models.Model):
    # user: A ForeignKey establishing a many-to-one relationship with the built-in User model in Django.
    # Each post is linked to a single user, and if a user is deleted, all their associated posts will also be deleted (on_delete=models.CASCADE).
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    # timestamp: This field stores the date and time of the post creation.
    # It has a default value of the current time (timezone.now).
    timestamp = models.DateTimeField(default=timezone.now)
    
    # content: A TextField used to store the content of the post.
    content = models.TextField()

    class Meta:
        # Meta class is used to specify the default ordering for the Post model.
        # In this case, the ordering is set to be in descending order based on the 'timestamp' field.
        ordering = ['-timestamp']

    def __str__(self):
        # __str__: Method overridden to return a string representation of the post.
        # It displays the username of the associated user and the content of the post.
        return f'{self.user.username}: {self.content}'

# Class Relationship: Represents the Relationship model in the Django application.
class Relationship(models.Model):
    # from_user: A ForeignKey establishing a many-to-one relationship with the built-in User model in Django.
    # Each relationship entry is linked to the user who initiates the relationship.
    # If a user is deleted, all their associated relationship entries will also be deleted (on_delete=models.CASCADE).
    from_user = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
    
    # to_user: A ForeignKey establishing a many-to-one relationship with the built-in User model in Django.
    # Each relationship entry is linked to the user who is the target of the relationship.
    # If a user is deleted, all relationship entries targeting them will also be deleted (on_delete=models.CASCADE).
    to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

    def __str__(self):
        # __str__: Method overridden to return a string representation of the relationship.
        # It displays the usernames of both the 'from_user' and 'to_user'.
        return f'{self.from_user} to {self.to_user}'

    class Meta:
        # Meta class is used to specify an index on the 'from_user' and 'to_user' fields to optimize query performance.
        indexes = [
            models.Index(fields=['from_user', 'to_user',]),
        ]











