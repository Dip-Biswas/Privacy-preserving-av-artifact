import re
from bs4 import BeautifulSoup
from . import Detector


class Sumsub(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://sumsub.com/

        sumsub_link_tags = soup.find_all(
            "link", attrs={"href": re.compile(r"\.sumsub\.com", re.I)}
        )

        sumsub_script = soup.find_all(
            "script", attrs={"src": re.compile(r"\.sumsub\.com", re.I)}
        )

        return {
            "link_tags": len(sumsub_link_tags) > 0,
            "scripts": len(sumsub_script) > 0,
            "subdomains": ".sumsub.com" in webpage,
        }


def test_sumsub_icon():
    icon = """
        <link rel="icon" href="https://static.sumsub.com/checkus/favicons/favicon.ico" sizes="any" type="image/x-icon" integrity="sha384-qHGZt64qFM6ra+rB2o8vDjX5BWvKgqsALGC6wrgp/7NeZ5MU4r/jW3a9ipTkUlk5" crossorigin="anonymous">
    """
    soup = BeautifulSoup(icon, "lxml")
    assert Detector.detect(Sumsub.run_checks(icon, soup))


def test_sumsub_js():
    script = r"""
    <script>
        window.__toAssetUrl = (path) => {
            const baseUrl = "https://static.sumsub.com/checkus/".replace(/\/$/, '');
            return `${baseUrl}/${path.replace(/^\//, '')}`;
        }
    </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Sumsub.run_checks(script, soup))


def test_sumsub_script():
    sumsub_script = """
        <script type="module" crossorigin="" src="https://static.sumsub.com/checkus/assets/entry-dee0py6o.js" integrity="sha384-HSFPSVj3V2v+L/Il/JImhCscJBuRTvx6aw7kS3eDnKZpj7UhsSEUyjn2OBWWJEJA"></script>
    """
    soup = BeautifulSoup(sumsub_script, "lxml")
    assert Detector.detect(Sumsub.run_checks(sumsub_script, soup))
