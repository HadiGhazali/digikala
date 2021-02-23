from emoji_picker.widgets import EmojiPickerTextarea

from .models import Comment
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=EmojiPickerTextarea)

    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': _('Comment'), }
        help_texts = {
            'text': _('Enter your comment.'),
        }
