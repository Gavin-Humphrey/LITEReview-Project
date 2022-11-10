from django import forms


class FollowForm(forms.Form):
    followed_user = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={"placeholder": "Rechercher un utilisateur"}),
    )
