from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.db import transaction


class CustomError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    @transaction.atomic
    def __init__(self, detail, field, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {force_str(field): force_str(detail)}
        else:
            self.detail = {"detail": force_str(self.default_detail)}

        transaction.set_rollback(True)
