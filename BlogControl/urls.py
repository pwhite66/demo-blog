from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from BlogControl.views import BlogDetailView, BlogListView, AjaxBlogRequestView, BlogCommentAddAjax, BlogCommentDeleteAjax

urlpatterns = [
    url(r'^$', BlogListView.as_view(), name='blog_list'),
    url(r'^ajax/$', AjaxBlogRequestView.as_view(), name='blog_list_ajax'),
    url(r'^details/(?P<slug>[-\w]+)/$', BlogDetailView.as_view(), name='blog_details'),
    url(r'^add_comment/(?P<slug>[-\w]+)/$', login_required(BlogCommentAddAjax.as_view()), name='blog_add_comment'),
    url(r'^delete_comment/(?P<slug>[-\w]+)/$', login_required(BlogCommentDeleteAjax.as_view()), name='blog_delete_comment'),
]
