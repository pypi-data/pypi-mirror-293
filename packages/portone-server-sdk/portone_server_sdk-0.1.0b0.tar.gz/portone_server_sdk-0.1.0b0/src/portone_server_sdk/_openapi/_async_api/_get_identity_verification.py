import dataclasses
from typing import Optional

from portone_server_sdk._api import ApiRequest, ApiErrorResponse, Empty
from portone_server_sdk import _errors
from portone_server_sdk._async import ApiClient
from portone_server_sdk._openapi._schemas._forbidden_error import ForbiddenError
from portone_server_sdk._openapi._schemas._get_identity_verification_error import GetIdentityVerificationError
from portone_server_sdk._openapi._schemas._identity_verification import IdentityVerification
from portone_server_sdk._openapi._schemas._identity_verification_not_found_error import IdentityVerificationNotFoundError
from portone_server_sdk._openapi._schemas._invalid_request_error import InvalidRequestError
from portone_server_sdk._openapi._schemas._unauthorized_error import UnauthorizedError

@dataclasses.dataclass
class GetIdentityVerificationParam:
    identity_verification_id: str = dataclasses.field(metadata={"serde_rename": "identityVerificationId"})
    """조회할 본인인증 아이디"""

@dataclasses.dataclass
class GetIdentityVerificationQuery:
    store_id: Optional[str] = dataclasses.field(metadata={"serde_rename": "storeId", "serde_skip_if": lambda value: value is None})
    """상점 아이디
    
    
    접근 권한이 있는 상점 아이디만 입력 가능하며, 미입력시 토큰에 담긴 상점 아이디를 사용합니다.
    """

@dataclasses.dataclass
class GetIdentityVerificationRequest(ApiRequest[IdentityVerification, GetIdentityVerificationError, GetIdentityVerificationParam, GetIdentityVerificationQuery, Empty]):
    method = "get"
    path = "/identity-verifications/{identityVerificationId}"

@dataclasses.dataclass
class GetIdentityVerification(ApiClient):
    async def get_identity_verification(
        self,
        identity_verification_id: str,
    ) -> Optional[IdentityVerification]:
        """본인인증 단건 조회
        
        주어진 아이디에 대응되는 본인인증 내역을 조회합니다.
        
        Args:
            identity_verification_id (str): 조회할 본인인증 아이디.
        
        Returns:
            성공 응답으로 본인 인증 객체 또는 `None`을 반환합니다.
        
        Raises:
            _errors.ForbiddenError: 요청이 거절된 경우
            _errors.InvalidRequestError: 요청된 입력 정보가 유효하지 않은 경우
            _errors.UnauthorizedError: 인증 정보가 올바르지 않은 경우
        """
        param_ = GetIdentityVerificationParam(
            identity_verification_id=identity_verification_id,
        )
        query_ = GetIdentityVerificationQuery(
            store_id=self.store_id,
        )
        body_ = Empty()
        response_ = await self.send(
            GetIdentityVerificationRequest(param_, query_, body_),
            IdentityVerification,
            GetIdentityVerificationError,
        )
        if isinstance(response_, ApiErrorResponse):
            error_ = response_.data
            if isinstance(error_, ForbiddenError):
                raise _errors.ForbiddenError(error_)
            elif isinstance(error_, IdentityVerificationNotFoundError):
                return None
            elif isinstance(error_, InvalidRequestError):
                raise _errors.InvalidRequestError(error_)
            else:
                raise _errors.UnauthorizedError(error_)
        else:
            return response_.data
