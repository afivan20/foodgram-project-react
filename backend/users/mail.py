from djoser.email import ActivationEmail


class MyMail(ActivationEmail):
    template_name = "email/activation.html"
