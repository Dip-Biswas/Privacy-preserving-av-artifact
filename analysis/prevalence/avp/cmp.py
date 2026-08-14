import re
from bs4 import BeautifulSoup
from . import Detector


class CmpAgeVerif(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # consentmanager.net bundles .cmpageverify* CSS classes in every deployment
        # regardless of whether the age-gate feature is enabled, so matching the CSS
        # selector string is too broad. Require an actual rendered element with that
        # class, which only appears when the gate is active.
        return {
            "class": len(soup.find_all(class_=re.compile(r"cmpageverif", re.I))) > 0
        }
