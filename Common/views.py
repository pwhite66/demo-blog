# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.views import LogoutView, LoginView, login
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic import FormView

from Common.forms import UserLoginForm, RegistrationForm


class CommonFormView(FormView):
    model = None
    add = False
    instance = None
    model_dict = None
    model_id = None

    def is_new(self):
        return self.add

    def get_form_kwargs(self):
        kwargs = super(CommonFormView, self).get_form_kwargs()
        # for a view that could have multiple models assigned models are added to the model_dict
        # then selected at this point
        if self.model_dict is not None:
            model_id = self.kwargs.pop('model_id', None)
            try:
                self.model = self.model_dict[model_id]
                self.model_id = model_id
            except KeyError:
                pass

        # get model via the primary key
        pk = self.kwargs.pop('pk', None)
        if pk is not None and self.model is not None:
            try:
                instance = self.model.objects.get(pk=pk)
                kwargs['instance'] = instance
                self.instance = instance
            except self.model.DoesNotExist:
                pass

        # get model via the slug field
        slug = self.kwargs.pop('slug', None)
        if slug is not None and self.model is not None:
            try:
                instance = self.model.objects.get(slug=slug)
                kwargs['instance'] = instance
                self.instance = instance
            except self.model.DoesNotExist:
                pass

        return kwargs


class BlogRegistrationView(FormView):
    template_name = "blog/registration.html"
    form_class = RegistrationForm

    def form_valid(self, form):
        login(self.request, form.user)
        return super(BlogRegistrationView, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog_list')


class BlogLoginView(LoginView):
    template_name = "blog/login.html"
    form_class = UserLoginForm


class BlogLogoutView(LogoutView):

    def get_next_page(self):
        return reverse('blog:blog_list')

class CommonJsonAjaxView(View):
    """
    renders the result of generate_json_return as a JSON object in the template. Used for passing JSON objects back
    using AJAX
    """
    def generate_json_return(self):
        raise ImproperlyConfigured("No json generated for output")

    def get(self, *args, **kwargs):

        js_string = self.generate_json_return()
        return HttpResponse(js_string, content_type="application/json")
