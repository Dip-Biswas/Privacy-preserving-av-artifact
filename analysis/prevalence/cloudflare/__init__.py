from bs4 import BeautifulSoup


def has_cloudflare_error(soup: BeautifulSoup) -> bool:
    title = soup.find("title")
    return title is not None and title.string == "Attention Required! | Cloudflare"
