from typing import Union
from portone_server_sdk._openapi._schemas._already_paid_error import AlreadyPaidError
from portone_server_sdk._openapi._schemas._forbidden_error import ForbiddenError
from portone_server_sdk._openapi._schemas._invalid_request_error import InvalidRequestError
from portone_server_sdk._openapi._schemas._unauthorized_error import UnauthorizedError

PreRegisterPaymentError = Union[AlreadyPaidError, ForbiddenError, InvalidRequestError, UnauthorizedError]
"""PreRegisterPaymentError"""

