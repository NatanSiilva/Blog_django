from django.forms import ModelForm
from .models import Comment


class FormComment(ModelForm):

    def clean(self):
        data = self.cleaned_data

        print(data)

    class Meta:
        model = Comment
        fields = ('name_comment', 'email_comment', 'comment',)
