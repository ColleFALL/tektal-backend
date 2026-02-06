from djoser import email
from core.emailer import send_brevo_email

class PasswordResetEmail(email.PasswordResetEmail):
    def send(self, to, *args, **kwargs):
        to_email = to[0]
        context = self.get_context_data()
        link = context.get("url")

        html = f"""
        <h2>Réinitialisation de mot de passe</h2>
        <p>Vous avez demandé à réinitialiser votre mot de passe.</p>
        <p><a href="{link}">Cliquez ici pour continuer</a></p>
        <p>Si ce n’est pas vous, ignorez cet email.</p>
        """

        send_brevo_email(
            to_email,
            "Mot de passe oublié – TEKTAL",
            html
        )
