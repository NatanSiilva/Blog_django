from django.forms import ModelForm
from .models import Comment


class FormComment(ModelForm):

    def clean(self):  # para validar o formulario
        data = self.cleaned_data
        name = data.get('name_comment')
        email = data.get('email_comment')
        comment = data.get('comment')

        if len(name) < 5:
            self.add_error('name_comment', 'Nome muito curto')

        if not comment or len(comment) < 10:
            self.add_error('comment', 'Comentario muito curto')

    class Meta:
        model = Comment
        fields = ('name_comment', 'email_comment', 'comment',)
