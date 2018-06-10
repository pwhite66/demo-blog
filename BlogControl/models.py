# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s by %s" % (self.title, self.author.username)

    @property
    def get_details(self):
        return {'title': self.title,
                'author': self.author.username,
                'created': self.date_created.strftime('%c')}

    class Meta:
        ordering = ('-date_created',)


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    slug = models.SlugField(default='')
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_created',)

    def get_details_string(self):
        return "by %s at %s" % (self.author.username, self.date_created.strftime('%H:%M %d/%m/%Y'))

    def save(self, *args, **kwargs):
        if self.slug in ['', None]:
            self.slug = get_random_string(length=32)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_details_string()


@admin.register(Blog, Comment)
class RecipeAdmin(admin.ModelAdmin):
    pass
