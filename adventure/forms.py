from django import forms
from django.db.models.fields import BooleanField
from .models import Choice

class ChoiceForm(forms.Form):
    choiceIndex = forms.ModelChoiceField(queryset=None)

    def __init__(self, name, *args, **kwargs):
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.fields['choiceIndex'] = forms.ModelChoiceField(label="Select Choice", queryset = Choice.objects.get(choiceName=name).choicepossibility_set.all(), required=True)
