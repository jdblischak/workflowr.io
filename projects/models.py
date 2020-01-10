from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.SlugField(primary_key=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:tag_detail', args=[str(self.name)])


class Publication(models.Model):
    doi = models.CharField('DOI', max_length=200)
    pmid = models.CharField('PMID', max_length=200, blank=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.doi


class Project(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField('URL')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    publications = models.ManyToManyField(Publication, blank=True)

    def __str__(self):
        return self.name
