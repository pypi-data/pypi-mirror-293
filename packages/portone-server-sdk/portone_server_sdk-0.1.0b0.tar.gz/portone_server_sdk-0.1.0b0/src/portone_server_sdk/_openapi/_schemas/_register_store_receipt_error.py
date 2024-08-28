from typing import Union
from portone_server_sdk._openapi._schemas._forbidden_error import ForbiddenError
from portone_server_sdk._openapi._schemas._invalid_request_error import InvalidRequestError
from portone_server_sdk._openapi._schemas._payment_not_found_error import PaymentNotFoundError
from portone_server_sdk._openapi._schemas._payment_not_paid_error import PaymentNotPaidError
from portone_server_sdk._openapi._schemas._pg_provider_error import PgProviderError
from portone_server_sdk._openapi._schemas._unauthorized_error import UnauthorizedError

RegisterStoreReceiptError = Union[ForbiddenError, InvalidRequestError, PaymentNotFoundError, PaymentNotPaidError, PgProviderError, UnauthorizedError]
"""RegisterStoreReceiptError"""

