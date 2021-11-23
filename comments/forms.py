from django.forms import ModelForm

from blog.settings import SECRET_KEY
from .models import Comment
import requests


class FormComment(ModelForm):

    def clean(self):  # para validar o formulario
        # data = self.cleaned_data
        raw_data = self.data
        recaptcha_response = raw_data.get('g-recaptcha-response')

        # if not recaptcha_response:
        #     self.add_error('comment', 'Por favor, marque a caixa "Não sou um robô"')

        
        recaptcha_request = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': '6LefLVIdAAAAAHMu4aBujDzs3dJjg_wBUyFa96T-',
                "response": recaptcha_response
            }
        )

        recaptcha_result = recaptcha_request.json()

        if not recaptcha_result['success']:
            self.add_error('comment', 'Desculpe Mr. Robot, ocorreu um erro')
            print(recaptcha_result)

        cleaned_data = self.cleaned_data
        name = cleaned_data.get('name_comment')
        email = cleaned_data.get('email_comment')
        comment = cleaned_data.get('comment')

        if len(name) < 5:
            self.add_error('name_comment', 'Nome muito curto')

        # if not comment or len(comment) < 10:
        #     self.add_error('comment', 'Comentario muito curto')

    class Meta:
        model = Comment
        fields = ('name_comment', 'email_comment', 'comment',)
