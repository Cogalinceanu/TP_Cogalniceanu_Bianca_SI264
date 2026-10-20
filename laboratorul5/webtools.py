
# Modul propriu pentru laboratorul Web
# Student: Numele vostru

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

TIMEOUT = 10

DEFAULT_HEADERS = {
    "User-Agent": "WebLab-Student"
}

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]


def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Descarcă URL-ul și returnează răspunsul HTTP."""
    return requests.get(
        url,
        timeout=timeout,
        headers=DEFAULT_HEADERS
    )


def get_status(url: str) -> int:
    """Returnează codul de stare HTTP."""
    return fetch(url).status_code


def get_title(html: str) -> str:
    """Extrage titlul HTML fără a depinde de majusculele tagurilor."""
    lower_html = html.lower()

    start = lower_html.find("<title>")
    end = lower_html.find("</title>")

    if start == -1 or end == -1 or end < start:
        return ""

    return html[start + len("<title>"):end].strip()


def page_exists(url: str) -> bool:
    """Verifică dacă URL-ul răspunde cu un cod HTTP mai mic decât 400."""
    try:
        return fetch(url).status_code < 400
    except requests.RequestException:
        return False


def check_paths(base: str, paths: list) -> dict:
    """Returnează codul HTTP pentru fiecare cale din listă."""
    results = {}

    for index, path in enumerate(paths):
        if index:
            time.sleep(1)

        url = urljoin(
            base.rstrip("/") + "/",
            path.lstrip("/")
        )

        try:
            results[path] = fetch(url).status_code
        except requests.RequestException:
            results[path] = None

    return results


def get_header(
    url: str,
    name: str,
    default: str = "lipsește"
) -> str:
    """Returnează valoarea unui antet HTTP."""
    try:
        return fetch(url).headers.get(name, default)
    except requests.RequestException:
        return default


def security_headers(url: str) -> dict:
    """Verifică prezența celor cinci antete de securitate."""
    try:
        headers = fetch(url).headers

        return {
            name: name in headers
            for name in SECURITY_HEADERS
        }
    except requests.RequestException:
        return {
            name: False
            for name in SECURITY_HEADERS
        }


def score_headers(results: dict) -> str:
    """Returnează scorul antetelor prezente, de exemplu 3/5."""
    total = len(results)
    present = sum(bool(value) for value in results.values())

    return f"{present}/{total}"


def fetch_robots(base: str):
    """Returnează robots.txt sau None dacă nu este disponibil."""
    url = urljoin(
        base.rstrip("/") + "/",
        "robots.txt"
    )

    try:
        response = fetch(url)

        if response.status_code == 200:
            return response.text

        return None
    except requests.RequestException:
        return None


def disallowed_paths(robots_text) -> list:
    """Extrage valorile Disallow din robots.txt; None produce o listă goală."""
    if not robots_text:
        return []

    result = []

    for line in robots_text.splitlines():
        line = line.strip()

        if line.lower().startswith("disallow:"):
            value = line.split(":", 1)[1].strip()

            if value:
                result.append(value)

    return result


def response_times(*urls: str) -> dict:
    """Măsoară timpul aproximativ de răspuns pentru fiecare URL."""
    result = {}

    for index, url in enumerate(urls):
        if index:
            time.sleep(1)

        start = time.perf_counter()

        try:
            fetch(url)
            result[url] = round(
                time.perf_counter() - start,
                4
            )
        except requests.RequestException:
            result[url] = None

    return result


def extract_links(html: str) -> list:
    """Extrage legăturile href unice și păstrează ordinea apariției."""
    links = re.findall(
        r'href=["\']([^"\']+)["\']',
        html,
        flags=re.IGNORECASE
    )

    return list(dict.fromkeys(links))


def split_links(links: list, domain: str) -> tuple:
    """Împarte legăturile în interne și externe."""
    base = domain if "://" in domain else "https://" + domain
    base_domain = urlparse(base).netloc.lower()

    internal = []
    external = []

    for link in links:
        absolute_url = urljoin(base, link)
        host = urlparse(absolute_url).netloc.lower()

        if not host or host == base_domain:
            internal.append(link)
        else:
            external.append(link)

    return internal, external


class ImageFinder(HTMLParser):
    """Colectează atributul src al tagurilor img."""

    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Colectează src când parserul întâlnește un tag img."""
        if tag.lower() == "img":
            src = dict(attrs).get("src")

            if src:
                self.images.append(src)


def page_fingerprint(url: str) -> str:
    """Calculează amprenta SHA-256 a corpului răspunsului."""
    response = fetch(url)
    response.raise_for_status()

    return hashlib.sha256(response.content).hexdigest()


def resolve(hostname: str) -> str:
    """Rezolvă un nume de domeniu într-o adresă IPv4."""
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

    expiry = datetime.fromtimestamp(
        expiry_timestamp,
        tz=timezone.utc
    )

    now = datetime.now(timezone.utc)

    return (expiry.date() - now.date()).days


def save_headers_json(
    headers: dict,
    filename: str = "headers.json"
) -> dict:
    """Salvează antetele în JSON, apoi citește și returnează conținutul."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            dict(headers),
            file,
            indent=2,
            ensure_ascii=False
        )

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def log(message: str, **details) -> None:
    """Afișează mesajul urmat de detaliile suplimentare."""
    extra = " | ".join(
        f"{key}={value}"
        for key, value in details.items()
    )

    print(message + (" | " + extra if extra else ""))


def site_report(
    url: str,
    json_filename: str = "report.json"
) -> dict:
    """Construiește, afișează și salvează un raport despre site."""

    report = {
        "requested_url": url,
        "status_code": None,
        "final_url": None,
        "title": "",
        "ip_address": None,
        "redirect_chain": [],
        "http_redirect_chain": [],
        "http_final_url": None,
        "security_headers": {},
        "security_score": "0/5",
        "certificate_days_left": None,
        "internal_links": 0,
        "external_links": 0,
        "disallowed_paths": [],
        "checked_at": datetime.now().isoformat(),
        "errors": [],
    }

    try:
        response = fetch(url)

        report["status_code"] = response.status_code
        report["final_url"] = response.url
        report["title"] = get_title(response.text)

        # Redirecționările efectuate la cererea principală
        for index, item in enumerate(response.history):
            if index + 1 < len(response.history):
                destination = response.history[index + 1].url
            else:
                destination = response.url

            report["redirect_chain"].append({
                "status_code": item.status_code,
                "from_url": item.url,
                "to_url": destination,
            })

        parsed = urlparse(response.url)
        hostname = parsed.hostname

        # Exercițiul DNS
        if hostname:
            try:
                report["ip_address"] = resolve(hostname)
            except (socket.gaierror, OSError) as error:
                report["errors"].append(
                    "DNS: " + str(error)
                )

            # Certificatul TLS
            if parsed.scheme == "https":
                try:
                    report["certificate_days_left"] = (
                        cert_days_left(hostname)
                    )
                except (
                    OSError,
                    ssl.SSLError,
                    ValueError,
                    KeyError
                ) as error:
                    report["errors"].append(
                        "Certificat TLS: " + str(error)
                    )

        # Antete de securitate
        header_results = {
            name: name in response.headers
            for name in SECURITY_HEADERS
        }

        report["security_headers"] = header_results
        report["security_score"] = score_headers(header_results)

        # Legături interne și externe
        links = extract_links(response.text)
        internal, external = split_links(links, response.url)

        report["internal_links"] = len(internal)
        report["external_links"] = len(external)

        # Fișierul robots.txt
        robots = fetch_robots(response.url)
        report["disallowed_paths"] = disallowed_paths(robots)

        # Verificare separată pentru HTTP -> HTTPS
        try:
            time.sleep(1)

            http_url = "http://" + (
                hostname or parsed.netloc
            )

            http_response = requests.get(
                http_url,
                timeout=TIMEOUT,
                headers=DEFAULT_HEADERS,
                allow_redirects=True
            )

            for index, item in enumerate(http_response.history):
                if index + 1 < len(http_response.history):
                    destination = (
                        http_response.history[index + 1].url
                    )
                else:
                    destination = http_response.url

                report["http_redirect_chain"].append({
                    "status_code": item.status_code,
                    "from_url": item.url,
                    "to_url": destination,
                })

            report["http_final_url"] = http_response.url

        except requests.RequestException as error:
            report["errors"].append(
                "Redirecționare HTTP: " + str(error)
            )

    except requests.RequestException as error:
        report["errors"].append(
            "Cerere HTTP: " + str(error)
        )

    # Salvarea raportului JSON
    try:
        with open(
            json_filename,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                report,
                file,
                indent=2,
                ensure_ascii=False
            )

    except OSError as error:
        print("Nu s-a putut salva raportul JSON:", error)

    # Afișarea raportului
    print(f"\n=== Raport site: {url} ===")
    print("Cod de stare:", report["status_code"])
    print("URL final:", report["final_url"])
    print("Titlu:", report["title"] or "(titlu negăsit)")
    print("Adresă IP:", report["ip_address"] or "(indisponibilă)")

    if report["http_redirect_chain"]:
        print("Redirecționări HTTP:")

        for item in report["http_redirect_chain"]:
            print(
                f'  {item["status_code"]}: '
                f'{item["from_url"]} -> {item["to_url"]}'
            )
    else:
        print(
            "Redirecționări HTTP: "
            "(niciuna detectată sau verificarea nu a reușit)"
        )

    print("URL final pentru HTTP:", report["http_final_url"])
    print("Antete de securitate:", report["security_headers"])
    print("Scor securitate:", report["security_score"])

    certificate_days = report["certificate_days_left"]

    if certificate_days is not None:
        print("Zile până la expirarea certificatului:", certificate_days)
    else:
        print("Certificat: (indisponibil)")

    print(
        f'Legături: {report["internal_links"]} interne, '
        f'{report["external_links"]} externe'
    )

    print(
        "Căi interzise:",
        ", ".join(report["disallowed_paths"]) or "(niciuna găsită)"
    )

    if report["errors"]:
        print("Atenționări:", " | ".join(report["errors"]))

    print("Raport JSON:", json_filename)

    return report


if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))