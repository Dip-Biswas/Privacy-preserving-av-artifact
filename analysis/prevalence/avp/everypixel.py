import re
from bs4 import BeautifulSoup
from . import Detector


class Everypixel(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://labs.everypixel.com/age_recognition
        # Age estimation API hosted at labs.everypixel.com/age_recognition
        # No embedded widget; purely API-based — integration appears in
        # inline JS fetch calls or server-side proxy references visible in source.

        everypixel_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r"labs\.everypixel\.com", re.I)}
        )

        return {
            "scripts": len(everypixel_scripts) > 0,
            "age_recognition_endpoint": "labs.everypixel.com/age_recognition" in webpage,
            "domain": "labs.everypixel.com" in webpage,
        }


def test_everypixel_api_call():
    fixture = """
        <script>
            const response = await fetch('https://labs.everypixel.com/age_recognition', {
                method: 'POST',
                headers: { 'Authorization': 'Basic ...' }
            });
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Everypixel.run_checks(fixture, soup))


def test_no_false_positive_everypixel():
    fixture = '<a href="https://everypixel.com/">stock photos</a>'
    soup = BeautifulSoup(fixture, "lxml")
    assert not Detector.detect(Everypixel.run_checks(fixture, soup))
