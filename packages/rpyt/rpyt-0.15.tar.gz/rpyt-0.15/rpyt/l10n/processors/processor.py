from abc import ABC, abstractmethod
from io import TextIOWrapper
from typing import Any

from rpyt.l10n.common import TlString


class Processor(ABC):
    extension: str

    @abstractmethod
    def read(self, file: str) -> dict[str, str]:
        pass

    @abstractmethod
    def write(
        self, file: str | TextIOWrapper, content: dict[str, Any]
    ) -> None:
        pass

    @abstractmethod
    def process(self, hashid: str, tlstring: TlString) -> Any:
        pass
