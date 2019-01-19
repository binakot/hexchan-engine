from django import forms


class TextareaWidget(forms.Textarea):
    template_name = 'imageboard/parts/textarea.html'
