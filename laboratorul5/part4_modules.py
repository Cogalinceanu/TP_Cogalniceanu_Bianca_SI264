import hashlib
import json
import re
import socket
import ssl
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10


def split_url(url: str) -> dict:
    """Descompune URL-ul în schemă, domeniu, cale, query și fragment."""
    parsed = urlparse(url)

    return {
        "scheme": parsed.scheme,
        "netloc": parsed.netloc,
        "path": parsed.path,
        "query": parsed.query,
        "fragment": parsed.fragment,
    }


def join_urls(base: str, links: list) -> list:
    """Transformă legăturile relative în URL-uri complete."""
    base_url = base.rstrip("/") + "/"
    return [urljoin(base_url, link) for link in links]


def extract_links(html: str) -> list:
    """Extrage legăturile href unice, păstrând ordinea."""
    found = re.findall(
        r'href=["\']([^"\']+)["\']',
        html,
        flags=re.IGNORECASE
    )

    return list(dict.fromkeys(found))


def split_links(links: list, domain: str) -> tuple:
    """Împarte legăturile în interne și externe."""
    base_url = domain if "://" in domain else "https://" + domain
    base_host = urlparse(base_url).netloc.lower()

    internal = []
    external = []

    for link in links:
        absolute_url = urljoin(base_url, link)
        link_host = urlparse(absolute_url).netloc.lower()

        if not link_host or link_host == base_host:
            internal.append(link)
        else:
            external.append(link)

    return internal, external


class ImageFinder(HTMLParser):
    """Parser HTML care colectează atributul src al tagurilor img."""

    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Este apelată automat la întâlnirea unui tag HTML de început."""
        if tag.lower() == "img":
            src = dict(attrs).get("src")

            if src:
                self.images.append(src)


def page_fingerprint(url: str) -> str:
    """Returnează amprenta SHA-256 a conținutului paginii."""
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()

    return hashlib.sha256(response.content).hexdigest()


def save_headers_json(
    response: requests.Response,
    filename: str = "headers.json"
) -> dict:
    """Salvează antetele în JSON, apoi le citește înapoi."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            dict(response.headers),
            file,
            indent=2,
            ensure_ascii=False
        )

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def resolve(hostname: str) -> str:
    """Returnează prima adresă IPv4 asociată numelui de domeniu."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Returnează numărul de zile până la expirarea certificatului TLS."""
    context = ssl.create_default_context()

    with socket.create_connection(
        (hostname, 443),
        timeout=TIMEOUT
    ) as sock:
        with context.wrap_socket(
            sock,
            server_hostname=hostname
        ) as secure_sock:
            certificate = secure_sock.getpeercert()

    expiry_timestamp = ssl.cert_time_to_seconds(
        certificate["notAfter"]
    )

    expiry_date = datetime.fromtimestamp(
        expiry_timestamp,
        tz=timezone.utc
    )

    now = datetime.now(timezone.utc)

    return (expiry_date.date() - now.date()).days


def main():
    """Execută exemplele pentru exercițiile 35-43."""

    # Exercițiul 35
    print("\n-- EXERCIȚIUL 35 --")
    print(split_url("https://cybercor.org/path?x=1#top"))

    # Exercițiul 36
    print("\n-- EXERCIȚIUL 36 --")
    print(
        join_urls(
            BASE_URL,
            ["/about", "contact.html", "../index.html"]
        )
    )

    try:
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        response.raise_for_status()

        # Exercițiul 37
        print("\n-- EXERCIȚIUL 37 --")
        links = extract_links(response.text)

        print("Legături găsite:", len(links))
        print(links[:30])

        # Exercițiul 38
        print("\n-- EXERCIȚIUL 38 --")
        internal, external = split_links(links, BASE_URL)

        print("Interne:", len(internal))
        print("Externe:", len(external))

        # Exercițiul 39
        print("\n-- EXERCIȚIUL 39 --")

        test_html = """
        <html><body>
          <img src="/logo.png" alt="Logo">
          <IMG SRC="poza.jpg">
          <img alt="imagine fără src">
          <img src="https://cdn.example.com/banner.webp" />
          <a href="/despre">Aceasta nu este o imagine</a>
        </body></html>
        """

        finder = ImageFinder()
        finder.feed(test_html)

        print("Imagini din HTML de test:", finder.images)

        assert finder.images == [
            "/logo.png",
            "poza.jpg",
            "https://cdn.example.com/banner.webp",
        ], "Parserul nu a găsit exact imaginile așteptate"

        print("Testul parserului a trecut!")

        finder_real = ImageFinder()
        finder_real.feed(response.text)

        print("Imagini găsite pe site:", len(finder_real.images))

        for src in finder_real.images:
            print(src)

        # Exercițiul 40
        print("\n-- EXERCIȚIUL 40 --")
        first = page_fingerprint(BASE_URL)

        time.sleep(1)

        second = page_fingerprint(BASE_URL)

        print("Amprenta 1:", first)
        print("Amprenta 2:", second)
        print("Identice:", first == second)
        print(
            "Amprentele pot diferi dacă pagina se modifică "
            "sau conține date dinamice."
        )

        # Exercițiul 41
        print("\n-- EXERCIȚIUL 41 --")
        headers = save_headers_json(response)

        print("Antet Server:", headers.get("Server", "lipsește"))
        print("Antetele au fost salvate în headers.json.")

        # Exercițiul 42
        print("\n-- EXERCIȚIUL 42 --")
        print("IP cybercor.org:", resolve("cybercor.org"))

        # Exercițiul 43
        print("\n-- EXERCIȚIUL 43 --")
        print(
            "Zile până la expirarea certificatului:",
            cert_days_left("cybercor.org")
        )

    except (
        requests.RequestException,
        OSError,
        socket.error,
        ssl.SSLError,
        ValueError,
        KeyError
    ) as error:
        print(
            "Unele exerciții nu au putut fi finalizate "
            "din cauza conexiunii sau a certificatului:",
            error
        )


if __name__ == "__main__":
    main()