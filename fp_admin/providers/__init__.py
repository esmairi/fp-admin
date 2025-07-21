from abc import ABC, abstractmethod
from typing import Any, Dict


# --- Provider Interface ---
class OAuth2Provider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique provider name (e.g., 'google', 'github')."""

    @abstractmethod
    def get_authorize_url(self, state: str) -> str:
        """Return the URL to redirect the user to for authorization."""

    @abstractmethod
    async def get_access_token(self, code: str) -> Dict[str, Any]:
        """Exchange code for access token."""

    @abstractmethod
    async def get_user_info(self, token: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch user info from the provider."""
