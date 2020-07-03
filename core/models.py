from django.db import models
from django.shortcuts import reverse
from cloudinary.models import CloudinaryField
import cloudinary.uploader


class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    slug = models.SlugField()
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    github = models.URLField(max_length=200)
    description = models.TextField()
    techs = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    image_url = models.TextField()
    image_url_alt = models.TextField(blank=True, null=True)
    image = CloudinaryField('image')

    """ Informative name for model """
    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Photo <%s:%s>" % (self.title, public_id)

    def __str__(self):
        return f"{self.id}: {self.title}"

    def get_absolute_url(self):
        return reverse("core:project-detail", kwargs={
            'slug': self.slug
        })
    
    class Meta:
        ordering = ['-id']


class Instagram(models.Model):
    title = models.CharField(max_length=50)
    embed = models.TextField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.id}: {self.title}"