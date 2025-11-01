from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nazwa")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tagi"
        ordering = ['name']

    def __str__(self):
        return self.name