import httpx
from typing import Generator

class BearerTokenAuth(httpx.Auth):
    def __init__(self, auth_url: str, client_id: str, client_secret: str):
        self.auth_url = auth_url
        self.client_id = client_id
        self.client_secret = client_secret
        self._token: str | None = None

    def _fetch_token(self) -> str:
        # Replace payload with your actual OAuth2 / Login endpoint structure
        response = httpx.post(
            self.auth_url,
            json={"client_id": self.client_id, "client_secret": self.client_secret},
            timeout=10.0
        )
        response.raise_for_status()
        self._token = response.json()["access_token"]
        return self._token

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        if not self._token:
            self._fetch_token()

        request.headers["Authorization"] = f"Bearer {self._token}"
        response = yield request

        # Auto-refresh on 401 Unauthorized and retry once
        if response.status_code == 401:
            self._fetch_token()
            request.headers["Authorization"] = f"Bearer {self._token}"
            yield request
