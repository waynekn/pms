from allauth.account.forms import LoginForm


class AllauthLoginForm(LoginForm):
    """
    Modify allauth form login placeholder to read 'Email or Username'
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update(
            {'placeholder': 'Email or Username'})
