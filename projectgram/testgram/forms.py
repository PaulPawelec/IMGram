from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image_post', 'description')

        widget = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class Post_Update_Form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('description',)

        widget = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class Comment_Add_Form(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment here',
                                                        'rows': '2', 'cols': '1'}))

    class Meta:
        model = Comment
        fields = ('text',)
