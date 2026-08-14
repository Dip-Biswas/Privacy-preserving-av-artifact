from . import has_rta_label


def test_rta():
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(
        '<meta name="RATING" content="RTA-5042-1996-1400-1577-RTA" />', "lxml"
    )
    assert has_rta_label(soup)
