import re
from bs4 import BeautifulSoup


def has_rta_label(soup: BeautifulSoup) -> bool:
    rta_meta_tags = soup.find_all(
        "meta",
        attrs={
            "name": re.compile(r"^RATING$", re.I),
            "content": re.compile(r"^mature|RTA-5042-1996-1400-1577-RTA$", re.I),
        },
    )
    pics_label_meta_tags = soup.find_all(
        "meta", attrs={"http-equiv": re.compile(r"^ pics-label$", re.I)}
    )

    return len(rta_meta_tags) > 0 or len(pics_label_meta_tags) > 0
