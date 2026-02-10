from djoser import email
from core.emailer import send_brevo_email
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings


class BrevoAPIEmailBackend(BaseEmailBackend):
    """
    Backend Django Email -> Brevo API.
    Djoser l'utilise pour activation + reset password.
    """

    def send_messages(self, email_messages):
        sent_count = 0

        for message in email_messages:
            to_emails = list(message.to) if message.to else []
            if not to_emails:
                continue

            subject = message.subject or ""
            body_html = message.alternatives[0][0] if getattr(message, "alternatives", None) else None
            html_content = body_html or (message.body or "")

            for to_email in to_emails:
                send_brevo_email(
                    to_email=to_email,
                    subject=subject,
                    html_content=html_content,
                )
                sent_count += 1

        return sent_count


class ActivationEmail(email.ActivationEmail):
    def send(self, to, *args, **kwargs):
        to_email = to[0] if isinstance(to, (list, tuple)) else to
        context = self.get_context_data()
        
        # ✅ CORRECTION : Récupérer uid et token séparément
        uid = context.get('uid')
        token = context.get('token')
        
        # ✅ CORRECTION : Construire le lien frontend avec query parameters
        frontend_url = getattr(settings, 'FRONTEND_URL', 'https://active-tektal.vercel.app')
        link = f"{frontend_url}/activate?uid={uid}&token={token}"

        html = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
          <h2>Activation de votre compte TEKTAL</h2>
          <p>Bienvenue sur TEKTAL ! Cliquez sur le lien ci-dessous pour activer votre compte :</p>
          <p>
            <a href="{link}" style="display:inline-block;padding:10px 14px;background-color:#FEBD00;color:#111111;text-decoration:none;border-radius:6px;font-weight:bold;">
              Activer mon compte
            </a>
          </p>
          <p>Si le bouton ne fonctionne pas, copiez-collez ce lien dans votre navigateur :</p>
          <p><a href="{link}" style="color:#FEBD00;">{link}</a></p>
          <p>Si vous n'êtes pas à l'origine de cette inscription, ignorez cet email.</p>
        </div>
        """

        send_brevo_email(
            to_email=to_email,
            subject="Activation de compte – TEKTAL",
            html_content=html,
        )


class PasswordResetEmail(email.PasswordResetEmail):
    def send(self, to, *args, **kwargs):
        to_email = to[0] if isinstance(to, (list, tuple)) else to
        context = self.get_context_data()
        
        # ✅ CORRECTION : Récupérer uid et token séparément
        uid = context.get('uid')
        token = context.get('token')
        
        # ✅ CORRECTION : Construire le lien frontend avec query parameters
        frontend_url = getattr(settings, 'FRONTEND_URL', 'https://active-tektal.vercel.app')
        link = f"{frontend_url}/reset-password?uid={uid}&token={token}"

        html = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
          <h2>Réinitialisation de mot de passe</h2>
          <p>Vous avez demandé à réinitialiser votre mot de passe TEKTAL.</p>
          <p>
            <a href="{link}" style="display:inline-block;padding:10px 14px;background-color:#FEBD00;color:#111111;text-decoration:none;border-radius:6px;font-weight:bold;">
              Réinitialiser mon mot de passe
            </a>
          </p>
          <p>Si le bouton ne fonctionne pas, copiez-collez ce lien dans votre navigateur :</p>
          <p><a href="{link}" style="color:#FEBD00;">{link}</a></p>
          <p>Si ce n'est pas vous, ignorez cet email.</p>
        </div>
        """

        send_brevo_email(
            to_email=to_email,
            subject="Mot de passe oublié – TEKTAL",
            html_content=html,
        )