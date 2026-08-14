import re
from bs4 import BeautifulSoup
from . import Detector


class CatchAll(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # Restrict to functional HTML contexts: script/iframe src, link/form href,
        # element id/class attributes, and page/section headings. Full-text search
        # fires on ToS prose, account-settings UI (Netflix, Tinder) and editorial
        # content that mention "age verification" without deploying any gate.
        pattern = re.compile(r"\bage[ -_]verif", re.I)
        in_src = (
            len(soup.find_all("script", attrs={"src": pattern})) > 0
            or len(soup.find_all("iframe", attrs={"src": pattern})) > 0
        )
        in_href = (
            len(soup.find_all(["a", "link"], attrs={"href": pattern})) > 0
            or len(soup.find_all("form", attrs={"action": pattern})) > 0
        )
        # Also match on attribute NAMES (e.g. data-age-verification-required set by JS)
        in_elem_attrs = (
            len(soup.find_all(True, attrs={"id": pattern})) > 0
            or len(soup.find_all(True, class_=pattern)) > 0
            or any(
                pattern.search(attr_name)
                for el in soup.find_all(True)
                for attr_name in el.attrs
            )
        )
        in_headings = any(
            pattern.search(el.get_text())
            for el in soup.find_all(["title", "h1", "h2", "h3"])
        )
        return {"wildcard": in_src or in_href or in_elem_attrs or in_headings}


def test_plain_text_no_match():
    # "Age Verification" in visible link text must not trigger
    fixture = '<a href="/">Age Verification</a>'
    soup = BeautifulSoup(fixture, "lxml")
    assert not Detector.detect(CatchAll.run_checks(fixture, soup))


def test_some_script():
    fixture = '<script src="/foo/age-verify.js"></script>'
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(CatchAll.run_checks(fixture, soup))


def test_element_id():
    fixture = '<div id="age-verification-modal"><button>I am 18+</button></div>'
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(CatchAll.run_checks(fixture, soup))


def test_element_class():
    fixture = '<div class="age-verif-gate"><button>Confirm age</button></div>'
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(CatchAll.run_checks(fixture, soup))
