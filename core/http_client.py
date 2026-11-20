import json
import logging
import allure
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config.settings import settings

logger = logging.getLogger("api_framework")

class APIClient:
    def __init__(self, base_url: str = settings.base_url, auth: httpx.Auth | None = None):
        self.client = httpx.Client(
            base_url=base_url,
            auth=auth,
            timeout=settings.timeout,
            headers={"Accept": "application/json"}
        )

    @retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type((httpx.TransportError, httpx.TimeoutException)),
        reraise=True
    )
    def request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        with allure.step(f"{method.upper()} {endpoint}"):
            logger.info(f"Request: {method.upper()} {endpoint} | Kwargs: {kwargs}")
            
            response = self.client.request(method, endpoint, **kwargs)
            
            # Attach details to Allure Report
            allure.attach(
                json.dumps(dict(response.request.headers), indent=2),
                name="Request Headers",
                attachment_type=allure.attachment_type.JSON
            )
            allure.attach(
                response.text,
                name=f"Response Body ({response.status_code})",
                attachment_type=allure.attachment_type.JSON
            )
            logger.info(f"Response: {response.status_code} | Time: {response.elapsed.total_seconds()}s")
            return response

    def get(self, endpoint: str, **kwargs) -> httpx.Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> httpx.Response:
        return self.request("POST", endpoint, **kwargs)

    def close(self):
        self.client.close()
