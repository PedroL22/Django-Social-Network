from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='static/images/default-pic.png', upload_to='profile_pics')
    phone = models.CharField('Phone', max_length=20)
    address = models.CharField('Address', max_length=20)
    bio = models.TextField('Bio', max_length=200)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    img1 = models.ImageField(upload_to='posts', blank=True, null=True)
    img2 = models.ImageField(upload_to='posts', blank=True, null=True)
    img3 = models.ImageField(upload_to='posts', blank=True, null=True)
    img4 = models.ImageField(upload_to='posts', blank=True, null=True)
    img5 = models.ImageField(upload_to='posts', blank=True, null=True)
    img6 = models.ImageField(upload_to='posts', blank=True, null=True)
    img7 = models.ImageField(upload_to='posts', blank=True, null=True)
    img8 = models.ImageField(upload_to='posts', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + ' | ' + str(self.author)