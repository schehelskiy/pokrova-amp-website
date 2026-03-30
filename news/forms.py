from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишіть ваш коментар тут...',
                # 👇 СТИЛІ ПРЯМО ТУТ (щоб точно працювало) 👇
                'style': 'background-color: #2b2b2b; color: #fff; border: 1px solid #444; resize: none;'
            })
        }
        labels = {
            'text': '' # Прибираємо підпис "Коментар" над полем
        }