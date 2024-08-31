import datetime
import phonenumbers
from typing import (Self, Any)
from pydantic import (Field, EmailStr, conint)
from pydantic_core import Url
from pydantic_extra_types.phone_numbers import PhoneNumber
from requests import Response
from .. import constants
from ..base import BaseInfuzuObject
from ..errors.base import InfuzuError
from ..http_requests import signed_requests
from ..utils.caching import CacheSystem


USER_CACHE: CacheSystem = CacheSystem(default_expiry_time=300)


class User(BaseInfuzuObject):
    user_id: str | None = Field(frozen=True, default=None)
    username: str | None = Field(frozen=True, default=None)
    email: EmailStr | None = Field(frozen=True, default=None)
    email_privacy_settings: str | None = Field(frozen=True, default=None)
    email_privacy_settings_display: str | None = Field(frozen=True, default=None)
    profile_photo: Url | None = Field(frozen=True, default=None)
    profile_photo_privacy_settings: str | None = Field(frozen=True, default=None)
    profile_photo_privacy_settings_display: str | None = Field(frozen=True, default=None)
    first_name: str | None = Field(frozen=True, default=None)
    middle_name: str | None = Field(frozen=True, default=None)
    last_name: str | None = Field(frozen=True, default=None)
    name_privacy_settings: str | None = Field(frozen=True, default=None)
    name_privacy_settings_display: str | None = Field(frozen=True, default=None)
    nickname: str | None = Field(frozen=True, default=None)
    nickname_privacy_settings: str | None = Field(frozen=True, default=None)
    nickname_privacy_settings_display: str | None = Field(frozen=True, default=None)
    date_of_birth: datetime.date | None = Field(frozen=True, default=None)
    date_of_birth_privacy_settings: str | None = Field(frozen=True, default=None)
    date_of_birth_privacy_settings_display: str | None = Field(frozen=True, default=None)
    gender: str | None = Field(frozen=True, default=None)
    gender_privacy_settings: str | None = Field(frozen=True, default=None)
    gender_privacy_settings_display: str | None = Field(frozen=True, default=None)
    phone_number: PhoneNumber | None = Field(frozen=True, default=None)
    phone_number_privacy_settings: str | None = Field(frozen=True, default=None)
    phone_number_privacy_settings_display: str | None = Field(frozen=True, default=None)
    record_storage_used: conint(ge=0) | None = Field(frozen=True, default=None)
    total_storage_used: conint(ge=0) | None = Field(frozen=True, default=None)
    cogitobot_storage_used: conint(ge=0) | None = Field(frozen=True, default=None)
    preferred_theme: str | None = Field(frozen=True, default=None)
    preferred_theme_display: str | None = Field(frozen=True, default=None)
    billing_in_good_status: bool | None = Field(frozen=True, default=None)
    signup_source: str | None = Field(frozen=True, default=None)
    policy_acceptance_version: datetime.date | None = Field(frozen=True, default=None)
    marketing_consent: bool | None = Field(frozen=True, default=None)
    marketing_preferences: dict[str, Any] | None = Field(frozen=True, default_factory=dict)

    @classmethod
    def retrieve(cls, user_id: str, force_new: bool = False) -> Self:
        def get_user() -> Self:
            api_response: Response = signed_requests.request(
                method="GET",
                url=f"{constants.USERS_BASE_URL}{constants.USERS_RETRIEVE_USER_ENDPOINT}".replace(
                    '<str:user_id>', user_id
                )
            )
            if api_response.status_code == 200:
                return cls(**api_response.json())
            raise InfuzuError(f"Error retrieving user: {api_response.text}")
        return USER_CACHE.get(
            cache_key_name=f'retrieve-{user_id}', specialized_fetch_function=get_user, force_new=force_new
        )

    def update(self, **fields) -> Self:
        for key, value in fields.items():
            if isinstance(value, datetime.datetime):
                fields[key] = value.isoformat()
            elif isinstance(value, datetime.date):
                fields[key] = value.isoformat()
            elif isinstance(value, PhoneNumber):
                fields[key] = phonenumbers.format_number(value, phonenumbers.PhoneNumberFormat.E164)

        def update_user() -> User:
            api_response: Response = signed_requests.request(
                method="POST",
                url=f"{constants.USERS_BASE_URL}{constants.USERS_RETRIEVE_USER_ENDPOINT}".replace(
                    '<str:user_id>', self.user_id
                ),
                json=fields
            )
            if api_response.status_code == 200:
                return User(**api_response.json())
            # TODO improve error handling
            raise InfuzuError(f"Error retrieving user: {api_response.text}")
        return USER_CACHE.get(
            cache_key_name=f'retrieve-{self.user_id}', specialized_fetch_function=update_user, force_new=True
        )

    def send_reset_email(self) -> str:

        api_response: Response = signed_requests.request(
            method="POST",
            url=f"{constants.USERS_BASE_URL}{constants.USERS_RESET_PASSWORD_ENDPOINT}".replace(
                '<str:email>', self.email
            ).replace('@', '%40')
        )
        if api_response.status_code == 200:
            return (
                    constants.USERS_BASE_URL + api_response.json()['url']
            ).replace('//', '/').replace(':/', '://')
        raise InfuzuError(f"Error retrieving user: {api_response.text}")
