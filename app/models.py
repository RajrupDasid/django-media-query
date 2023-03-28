from django.db import models
import uuid
import os
from django.template.defaultfilters import slugify
import random
import string
from django.utils.crypto import get_random_string
import base64
# Create your models here.
from django.conf import settings

def file_upload_location(instance, filename):
    file_description = instance.details.name.lower().replace(" ", "-")
    file_name = filename.lower().replace(" ", "-")
    return os.path.join("New_files", file_description, file_name)


class FileDetail(models.Model):
    auth_user= models.ForeignKey(settings.AUTH_USER_MODEL, default=None,on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default=None)
    number_folder = models.CharField(max_length=255, default=None)
    created = models.DateTimeField(auto_now_add=True)
    upadate = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"file name {self.name}"


class FileUpload(models.Model):
    auth_user= models.ForeignKey(settings.AUTH_USER_MODEL,default=None, on_delete=models.CASCADE)
    details = models.ForeignKey(FileDetail, default=None, on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_upload_location, null=True, blank=True)

    def __str__(self) -> str:
        return f"name of files uploaded are {self.file}"


def photo_upload_location(instance, image_name):

    url = instance.details.name
    image_name = f'{uuid.uuid5(uuid.NAMESPACE_URL,url).hex}.jpg'
    return os.path.join('gallery_images', image_name)


class PhotoDetails(models.Model):
    auth_user= models.ForeignKey(settings.AUTH_USER_MODEL, default=None,on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default=None)
    description = models.TextField(default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    upadate = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"photo names are {self.name}"

    class Meta:
        verbose_name = 'Photo Detail'
        verbose_name_plural = 'Photo Details'


class Photo(models.Model):
    auth_user= models.ForeignKey(settings.AUTH_USER_MODEL, default=None,on_delete=models.CASCADE)
    details = models.ForeignKey(PhotoDetails, default=None, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=photo_upload_location, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    upadate = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"photo details are {self.details}"


def random_gen(size=25):
    return ''.join(get_random_string(size))


def video_upload_location(instance, filename):
    video_description = random_gen()
    random_video_name = get_random_string(22)
    video_name = filename.lower().replace(" ", random_video_name)
    return os.path.join("new_video_files", video_description, video_name)


def video_thumbnail_upload_location(instance, filename):
    rand_chars = get_random_string(10)
    image_file_area = rand_chars
    random_image_name = get_random_string(25)
    image_name = filename.lower().replace("-", random_image_name)
    return os.path.join("video_thumbnails", image_file_area, image_name)


def random_string_generator(size=30, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class VideoFileDetails(models.Model):
    auth_user= models.ForeignKey(settings.AUTH_USER_MODEL,default=None ,on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    upadate = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"file name {self.name}"

    class Meta:
        verbose_name = 'Video File Detail'
        verbose_name_plural = 'Video file Details'


class VideoUpload(models.Model):
    auth_user= models.ForeignKey(settings.AUTH_USER_MODEL, default=None ,on_delete=models.CASCADE)
    details = models.ForeignKey(VideoFileDetails, default=None, on_delete=models.CASCADE)
    video_thumbnail = models.ImageField(upload_to=video_thumbnail_upload_location, null=True, blank=True, default=None)
    slug = models.SlugField(max_length=1000, unique=True, blank=True)
    file = models.FileField(upload_to=video_upload_location, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    upadate = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"name of files uploaded are {self.file}"

    def save(self, *args, **kwargs):
        original_slug = slugify(random_string_generator())
        queryset = VideoUpload.objects.all().filter(slug__iexact=original_slug).count()
        count = 1
        slug = original_slug
        while (queryset):
            slug = original_slug + '-' + str(count) + "-".join(random_string_generator())
            count += 1
            queryset = VideoUpload.objects.all().filter(slug__iexact=slug).count()
        self.slug = slug
        super().save(*args, **kwargs)
