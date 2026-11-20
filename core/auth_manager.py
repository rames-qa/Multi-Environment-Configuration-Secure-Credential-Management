from typing import Generator
import httpx
class BearerTokenAuth(httpx.Auth):
    def __init__(
        self,
        auth_url: str,
        client_id: str,
        client_secret: str,
        timeout: float = 10.0,
        token_field: str = "access_token",
    ):
        self.auth_url = auth_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout = timeout
        self.token_field = token_field
        self._token: str | None = None

    def _fetch_token(self) -> str:
        # Adjust payload and token_field to match your auth server's contract
        response = httpx.post(
            self.auth_url,
            json={"client_id": self.client_id, "client_secret": self.client_secret},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        if self.token_field not in payload:
            raise KeyError(
                f"Expected '{self.token_field}' in auth response keys: {list(payload.keys())}"
            )
        self._token = payload[self.token_field]
        return self._token

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        if not self._token:
            self._fetch_token()

        request.headers["Authorization"] = f"Bearer {self._token}"
        response = yield request

        # Refresh once if the token expired and returned 401 Unauthorized
        if response.status_code == 401:
            self._fetch_token()
            request.headers["Authorization"] = f"Bearer {self._token}"
            yield request
