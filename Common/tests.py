# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse

from Common.forms import UserLoginForm
from Common.views import BlogRegistrationView, BlogLoginView


class BlogRegistrationViewTest(TestCase):
    """
    Test for the Blog List View
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_get(self):
        request = self.factory.get(reverse('register'))
        response = BlogRegistrationView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class BlogLoginViewTest(TestCase):
    """
    Test for the Blog List View
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='user_test', password='password1234')

    def test_get(self):
        request = self.factory.get(reverse('login'))
        response = BlogLoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class LoginFormTest(TestCase):

    def test_form(self):
        form = UserLoginForm(data={'username': "user_test", 'password': "password1234"})
        self.assertTrue(form.is_valid())


class BlogLogoutViewTest(TestCase):
    """
    Test for the Blog List View
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_get(self):
        request = self.factory.get(reverse('logout'))
        response = BlogLoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)
