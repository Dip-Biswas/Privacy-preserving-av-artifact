import json

from bs4 import BeautifulSoup

from . import run_detectors, check_soup, check_site
from prevalence.avp import COLUMN_NAMES, PROVIDER_NAMES, BlueCheck, Veriff, Yoti

rta_veriff_bluecheck = """
    <head>
        <meta name="RATING" content="RTA-5042-1996-1400-1577-RTA" />
        <script data-n-head="1" src="https://cdn.veriff.me/incontext/js/v1/veriff.js"></script>
        <script src="https://verify.bluecheck.me/platforms/lightspeed/js/AgeVerification.js?domain_token=YOUR_DOMAIN_TOKEN_HERE"></script>
    </head>
"""


def test_columns_present():
    result = run_detectors("example.com", rta_veriff_bluecheck)
    for col in COLUMN_NAMES:
        assert col in result


def test_name():
    result = run_detectors("example.com", rta_veriff_bluecheck)
    assert result["name"] == "example.com"


def test_rta_doesnt_short_circuit():
    result = run_detectors("example.com", rta_veriff_bluecheck)
    assert result[Veriff.name()]


def test_multiple_providers():
    result = run_detectors("example.com", rta_veriff_bluecheck)
    assert result[Veriff.name()] and result[BlueCheck.name()]


def test_run_detectors_type():
    result = run_detectors("example.com", rta_veriff_bluecheck)
    assert result[Veriff.name()] == 1
    assert result[BlueCheck.name()] == 1


def test_meta_info():
    result = run_detectors("example.com", rta_veriff_bluecheck)

    assert "meta_info" in result
    assert type(result["meta_info"]) is str

    meta_info = json.loads(result["meta_info"])

    assert BlueCheck.name() in meta_info
    assert len(meta_info[BlueCheck.name()]) > 0

    assert Veriff.name() in meta_info
    assert len(meta_info[Veriff.name()]) > 0


def test_check_soup():
    soup = BeautifulSoup(rta_veriff_bluecheck, "lxml")
    result_name, (result, passed_checks) = check_soup(
        (BlueCheck, (rta_veriff_bluecheck, soup))
    )

    assert result_name == BlueCheck.name()
    assert result is True
    assert len(passed_checks) > 0
    assert "subdomains" in passed_checks


def test_check_site():
    params = "prevalence/fixtures", "xhamster1.desi.html"
    result = check_site(params)

    for col in COLUMN_NAMES:
        assert col in result

    assert result[Yoti.name()] and (not result["cloudflare"])


def test_check_site_col_types():
    params = "prevalence/fixtures", "xhamster1.desi.html"
    result = check_site(params)

    for col in PROVIDER_NAMES:
        assert type(result[col]) is int

    assert type(result["parse_error"]) is int
    assert type(result["cloudflare"]) is int
    assert type(result["rta"]) is int
