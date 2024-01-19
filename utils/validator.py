from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details


class ValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'invalid'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and isinstance(detail, list):
            detail = [detail]
        else:
            detail = detail

        self.detail = _get_error_details(detail, code)
