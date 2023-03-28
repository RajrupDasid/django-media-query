from django.db import models
from django.conf import settings
from PIL import Image as Img
from io import BytesIO
import random
import string
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

# Create your models here.


def random_string_generator(size=100, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class UserProfile(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join("UserProfile", self.userdetails.email, instance)
    userdetails=models.ForeignKey(settings.AUTH_USER_MODEL, default=None,on_delete=models.CASCADE)
    bio = models.TextField(default=None,blank=True,null=True)
    profile_image=models.ImageField(upload_to=image_upload_to,default=None)
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User Profile Details: {self.userdetails.email}"
    
    def save(self, *args, **kwargs):
        if self.profile_image:
            img = Img.open(BytesIO(self.profile_image.read()))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.profile_image((self.profile_image.width / 1.5, self.profile_image.height / 1.5), Img.ANTIALIAS)
            output = BytesIO()
            img.save(output, format='WebP', quality=80)
            output.seek(0)
            self.profile_image = InMemoryUploadedFile(output, 'ImageField', "%s.webp" % self.profile_image.name.join(
                random_string_generator()).split('.')[0:10], 'profile_image/webp', len(output.getbuffer()), None)
        super().save(*args, **kwargs)