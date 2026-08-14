from bs4 import BeautifulSoup
from . import Detector


class Ep(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # spotted on 'eporner'
        has_age_verify_elem_ids = len(soup.find_all(id="ageverifyusa")) > 0

        return {"id_elems": has_age_verify_elem_ids}
