import logging
from typing import TypeVar

import httpx
from pydantic import BaseModel

from .models import Root, Task

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=BaseModel)


class ProcessingClient(object):
    def __init__(
        self, url: str, auth: httpx.Auth | None = None, timeout: int = 10
    ) -> None:
        logger.debug(
            f"Connecting to scse-processing instance at '{url}' using "
            f"auth class `{auth}`..."
        )
        self.url = url
        self.auth = auth
        self.client = httpx.Client(
            base_url=self.url,
            timeout=timeout,
            http2=True,
            auth=auth,
            follow_redirects=True,
        )

        self.check_root()

    def check_root(self):
        """Requests root api endpoint."""
        res = self.client.get("/")
        res.raise_for_status()
        root = Root(**res.json())
        return root

    def start_basic_task(self) -> Task:
        res = self.client.post("tasks/basic")
        res.raise_for_status()
        return Task(**res.json())

    def start_sleep_task(self, seconds: int = 1) -> Task:
        res = self.client.post("tasks/sleep", json={"seconds": seconds})
        res.raise_for_status()
        return Task(**res.json())

    def retrieve_task(self, id: str) -> Task:
        res = self.client.get(f"tasks/{id}/")
        res.raise_for_status()
        return Task(**res.json())
