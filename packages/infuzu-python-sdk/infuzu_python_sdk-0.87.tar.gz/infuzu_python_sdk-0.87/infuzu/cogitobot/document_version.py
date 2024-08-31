import datetime
from typing import Any
from pydantic import Field
from requests import Response
from .. import constants
from ..base import BaseInfuzuObject
from ..errors.base import InfuzuError
from ..http_requests import signed_requests


class DocumentVersion(BaseInfuzuObject):
    id: str | None = Field(frozen=True, default=None)
    document: str | None = Field(frozen=True, default=None)
    vector_store_version: str | None = Field(frozen=True, default=None)
    page_content: str | None = Field(frozen=True, default=None)
    meta_data: dict[str, Any] | None = Field(frozen=True, default=None)
    created_at: str | None = Field(frozen=True, default=None)

    @property
    def created_at_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self.created_at)

    @classmethod
    def retrieve(cls, id: str, private_key: str = None) -> 'DocumentVersion':
        api_response: Response = signed_requests.request(
            method="GET",
            url=f"{constants.COGITOBOT_BASE_URL}"
                f"{constants.COGITOBOT_RETRIEVE_DOCUMENT_VERSION_ENDPOINT.replace('<str:document_version_id>', id)}",
            private_key=private_key
        )
        if api_response.status_code == 200:
            return cls(**api_response.json())
        raise InfuzuError(f"There was an error retrieving the document version {api_response.text}")
