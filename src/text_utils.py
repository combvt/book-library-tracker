import html
from bs4 import BeautifulSoup

def strip_html(text: str) -> str:
    if not text:
        return ""
    
    text = html.unescape(text)

    soup = BeautifulSoup(text, "html.parser")

    return soup.get_text()


