from django import forms
from Store.models import Game
from django.core.exceptions import ValidationError
import json

MAX_JSON_DATA_LEN = 2048


class MessageForm(forms.Form):
    # Every message should conform to this basic form. We use it as a base class for all the other forms about messaging
    messageType = forms.ChoiceField(required=True, choices=[('SCORE','score'), ('SAVE','save'), ('LOAD_REQUEST','load_request')], widget=forms.HiddenInput())


class MessageScoreForm(MessageForm):
    score = forms.DecimalField(required=True, widget=forms.HiddenInput())

    def clean_messageType(self):
        if self.cleaned_data['messageType'] != 'SCORE':
            raise ValidationError("MessageScoreForm should be created by a SCORE message type.")
        return self.cleaned_data['messageType']


class MessageSaveForm(MessageForm):
    gameState = forms.CharField(required=True, widget=forms.HiddenInput(), max_length=MAX_JSON_DATA_LEN)

    def clean_messageType(self):
        if self.cleaned_data['messageType'] != 'SAVE':
            raise ValidationError("MessageSaveForm should be created by a SAVE message type.")
        return self.cleaned_data['messageType']

    def clean_gameState(self):
        # Check if the game state is serializable by json and if the length is ok
        try:
            # Check for validity
            tmp = json.loads(self.cleaned_data['gameState'])
        except ValueError:
            raise ValidationError("The game state is not valid json and I refuse to store it.")

        if len(self.cleaned_data['gameState']) > MAX_JSON_DATA_LEN:
            raise ValidationError("The gameState you are trying to save is too large.")

        return self.cleaned_data['gameState']

# Implementing the following class just for consistency. It is not necessary, but I prefer to keep the code linear and
# consistent
class MessageLoadForm(MessageForm):

    def clean_messageType(self):
        if self.cleaned_data['messageType'] != 'LOAD_REQUEST':
            raise ValidationError("MessageSaveForm should be created by a LOAD_REQUEST message type.")

        return self.cleaned_data['messageType']