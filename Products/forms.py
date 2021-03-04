from emoji_picker.widgets import EmojiPickerTextarea

from .models import Comment, Product, Brand
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

User = get_user_model()
BIRTH_YEAR_CHOICES = ['create_at', 'low_price', 'high_price', 'hit_count']


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


ORDER_BY = ((
    ('create_at', 'جدیدترین ها'),
    ('hit_count', 'پربازدید ترین ها'),
    ('high_price', 'گران ترین ها'),
    ('low_price', 'ارزان ترین ها')
))


class FilterForm(forms.Form):
    brand = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    order_by = forms.MultipleChoiceField(required=False,
                                         widget=forms.RadioSelect,
                                         choices=ORDER_BY)
