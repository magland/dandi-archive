from __future__ import annotations

from rest_framework import status

from dandiapi.api.services.exceptions import DandiError


class DandisetNotEmbargoedError(DandiError):
    http_status_code = status.HTTP_400_BAD_REQUEST
    message = 'Dandiset not embargoed'
