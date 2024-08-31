from pydantic import Field
from requests import Response
from .. import constants
from ..base import BaseInfuzuObject
from ..errors.base import InfuzuError
from ..http_requests import signed_requests
from ..utils.caching import CacheSystem


USER_ACCESS_PROFILE_CACHE: CacheSystem = CacheSystem(default_expiry_time=60)


class UserAccessProfile(BaseInfuzuObject):
    user_id: str | None = Field(frozen=True, default=None)
    billing_in_good_standing: bool | None = Field(frozen=True, default=None)
    active_subscriptions: list[str] | None = Field(frozen=True, default=None)

    @classmethod
    def retrieve(cls, user_id: str, force_new: bool = False) -> 'UserAccessProfile':
        if not user_id:
            user_id: str = 'null'

        def get_user_access_profile() -> 'UserAccessProfile':
            api_response: Response = signed_requests.request(
                method="GET",
                url=f"{constants.ACCESS_BASE_URL}"
                    f"{constants.ACCESS_RETRIEVE_USER_ACCESS_PROFILE_ENDPOINT}".replace('<str:user_id>', user_id)
            )
            if api_response.status_code == 200:
                return cls(**api_response.json())
            raise InfuzuError(f"Error retrieving user access profile: {api_response.text}")
        return USER_ACCESS_PROFILE_CACHE.get(
            cache_key_name=f'{user_id}', specialized_fetch_function=get_user_access_profile, force_new=force_new
        )
