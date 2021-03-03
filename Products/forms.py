from emoji_picker.widgets import EmojiPickerTextarea

from .models import Comment, Product
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


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('slug', 'brand', 'category', 'name', 'image', 'details', 'review')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
            'review': forms.Textarea(attrs={'class': 'form-control'}),
        }
