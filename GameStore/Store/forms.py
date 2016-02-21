from django import forms
from django.contrib.auth.models import Group
from Users.models import Profile
from .models import Game, Category
from django.core.exceptions import ValidationError

"""
Django cleaning call stack
-> clean_<fieldname>()  : used to check validity of the file itself
-> clean()              : used to check validity over multiple fields
-> validate_unique()    : used to check validity of the whole object
"""


class GameForm(forms.ModelForm):
    # Need to check max_length of name, otherwise the django model will truncate the name
    name = forms.CharField(required=True, max_length=80)
    description = forms.CharField(required=True, widget=forms.Textarea())
    # We redefine price so we can define the maximum number of decimals
    price = forms.DecimalField(required=True, decimal_places=2, max_digits=9)

    # Populate at runtime
    _category = forms.ModelChoiceField(required=True, queryset=None)

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        # Dynamically populate the category set
        self.fields['_category'].queryset = Category.objects.all()

    """
    Custom uniqueness check of game's name and url.
    Custom check for only-positive price
    """

    def clean_price(self):
        if float(self.cleaned_data['price']) < 0:
            raise ValidationError("Price must be positive.")
        return self.cleaned_data['price']

    class Meta:
        model = Game
        fields = ('name', 'description', 'url', 'price', 'logo', '_category')


class CartForm(forms.Form):
    action = forms.ChoiceField(choices=[('add','Add'), ('remove', 'Remove')], required=True)
    game = forms.ModelChoiceField(required=True, queryset=None)

    def __init__(self, *args, **kwargs):
        super(CartForm, self).__init__(*args, **kwargs)
        # Dynamically populate the category set
        self.fields['game'].queryset = Game.objects.all()