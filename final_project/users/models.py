from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core import validators


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True, default="")
    logged_on = models.BooleanField(default=False)
    friends = models.CharField(max_length=500, validators=[validators.validate_comma_separated_integer_list], default="")
    bio = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.username = self.user.username

        img = Image.open(self.image.path)

        # limits the size of the profile photo to 300px by 300px
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
