# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse

from BlogControl.models import Blog, Comment
from BlogControl.views import BlogListView, BlogDetailView


class BlogListViewTest(TestCase):
    """
    Test for the Blog List View
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_get(self):
        request = self.factory.get(reverse('blog:blog_list'))
        response = BlogListView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class BlogDetailViewTest(TestCase):
    """
    Test for the Blog Details View
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='user_test', password='password1234')
        self.blog = Blog.objects.create(slug='example', body="body", author=self.user)
        self.comment = Comment.objects.create(comment='comment_text', author=self.user, blog=self.blog)

    def test_get(self):
        request = self.factory.get(reverse('blog:blog_details', kwargs={'slug': self.blog.slug}))
        response = BlogDetailView.as_view()(request, slug=self.blog.slug)
        self.assertEqual(response.status_code, 200)
        self.assertIsNot(response.context_data['object'], None)
        self.assertEqual(len(response.context_data['view'].get_comment_list()), 1)
        self.assertEqual(response.context_data['view'].get_comment_list()[0].comment, self.comment.comment)
