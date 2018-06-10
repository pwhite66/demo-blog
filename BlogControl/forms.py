from django import forms

from BlogControl.models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']