from oauth2_provider.signals import app_authorized
from django.dispatch import receiver
from seguridad.util import registra_session

# @receiver(app_authorized)
# def handle_token_obtained(sender, request, token, **kwargs):
#     user = token.user
#     registra_session(request)