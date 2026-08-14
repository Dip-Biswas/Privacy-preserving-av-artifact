from abc import abstractmethod
from typing import NewType

from bs4 import BeautifulSoup


class Detector:
    @classmethod
    def name(cls) -> str:
        return cls.__name__

    @staticmethod
    @abstractmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        return {}

    @staticmethod
    def detect(check_results: dict[str, bool]) -> bool:
        return any(check_results.values())

    @staticmethod
    def passed_checks(check_results: dict[str, bool]) -> list[str]:
        passed_checks = [k for k, v in check_results.items() if v]
        return passed_checks


ADetector = NewType("ADetector", Detector)
