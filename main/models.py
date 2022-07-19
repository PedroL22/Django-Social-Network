from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='static/images/default-pic.png', upload_to='profile_pics', blank=True, null=True)
    phone = models.CharField('Phone', max_length=20)
    address = models.CharField('Address', max_length=20)
    bio = models.TextField('Bio', max_length=200)

    def __str__(self):
        return self.user.username

    # def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    img = models.ImageField(upload_to='posts', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date) + ' | ' + str(self.author)
