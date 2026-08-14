import re
from bs4 import BeautifulSoup
from . import Detector


class Generic(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        pattern = re.compile("age-verif")

        scripts_with_av_names = soup.find_all("script", attrs={"src": pattern})
        stylesheets_with_av_names = soup.find_all("link", attrs={"href": pattern})
        elems_with_data_age_verif = soup.find_all(
            attrs={"data-": re.compile(r"age.verif")}
        )

        return {
            "scripts": len(scripts_with_av_names) > 0,
            "stylesheets": len(stylesheets_with_av_names) > 0,
            "data_ageverif": len(elems_with_data_age_verif) > 0,
        }
