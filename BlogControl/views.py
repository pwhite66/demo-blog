# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import datetime

from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView

from BlogControl.forms import CommentForm
from BlogControl.models import Blog, Comment
from Common.views import CommonJsonAjaxView

BLOG_STATUS_NEW = 1
BLOG_STATUS_MODIFIED = 2


class BlogListView(TemplateView):
    template_name = 'blog/list.html'


class AjaxBlogRequestView(CommonJsonAjaxView):
    def generate_json_return(self):
        json_dict = {}
        if self.request.GET['date'] == '':
            # initial check so get all blogs
            new_blogs = Blog.objects.all()
            mod_blogs = None
        else:
            # blog update so only get changed or added blogs
            date_str = self.request.GET['date']
            date_obj = datetime.strptime(date_str, '%d/%m/%Y, %H:%M:%S')
            new_blogs = Blog.objects.filter(date_created__gte=date_obj)
            mod_blogs = Blog.objects.filter(date_modified__gte=date_obj)

        for blog in new_blogs:
            json_dict[blog.slug] = blog.get_details
            json_dict[blog.slug]['status'] = BLOG_STATUS_NEW

        if mod_blogs is not None:
            for blog in mod_blogs:
                json_dict[blog.slug] = blog.get_details
                json_dict[blog.slug]['status'] = BLOG_STATUS_MODIFIED

        return json.dumps(json_dict)


class BlogDetailView(DetailView):
    template_name = 'blog/detail.html'
    model = Blog

    @staticmethod
    def get_comment_form():
        return CommentForm()

    def get_comment_list(self):
        return Comment.objects.filter(blog=self.object)


class BlogCommentAddAjax(FormView):
    template_name = "base/base_modal_form.html"
    form_class = CommentForm
    model = Comment

    def form_valid(self, form):
        result = {'status': 'SUCCESS'}
        try:
            blog = Blog.objects.get(slug=self.kwargs['slug'])
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = self.request.user
            comment.save()

            result['comment'] = comment.comment
            result['details'] = comment.get_details_string()
            result['comment_id'] = comment.id
            result['delete_url'] = reverse('blog:blog_delete_comment', kwargs={'slug': comment.slug})
        except Blog.DoesNotExist:
            result['status'] = 'FAILED'

        return_json = json.dumps(result)
        return HttpResponse(return_json, content_type="application/json")


class BlogCommentDeleteAjax(CommonJsonAjaxView):
    def generate_json_return(self):
        comment = Comment.objects.get(slug=self.kwargs['slug'])
        comment.delete()

        return_json = json.dumps({'status': 'SUCCESS'})
        return HttpResponse(return_json, content_type="application/json")

