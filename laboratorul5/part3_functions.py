
# Laborator: funcții, metode și importuri pe web
# Student: Numele vostru

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]


def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Descarcă o pagină și returnează obiectul Response."""
    return requests.get(url, timeout=timeout)


def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa primită."""
    return fetch(url).status_code


def get_title(html: str) -> str:
    """Extrage titlul dintre tagurile title dintr-un șir HTML."""
    lower_html = html.lower()
    start = lower_html.find("<title>")
    end = lower_html.find("</title>")

    if start == -1 or end == -1 or end < start:
        return ""

    return html[start + len("<title>"):end].strip()


def page_exists(url: str) -> bool:
    """Returnează True dacă URL-ul răspunde cu un cod mai mic decât 400."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        return response.status_code < 400
    except requests.RequestException:
        return False


def check_paths(base: str, paths: list) -> dict:
    """Returnează codul HTTP pentru fiecare cale relativă din listă."""
    results = {}

    for index, path in enumerate(paths):
        if index:
            time.sleep(1)

        url = base.rstrip("/") + "/" + path.lstrip("/")

        try:
            response = requests.get(url, timeout=TIMEOUT)
            results[path] = response.status_code
        except requests.RequestException:
            results[path] = None

    return results


def get_header(
    url: str,
    name: str,
    default: str = "lipsește"
) -> str:
    """Returnează valoarea unui antet HTTP sau valoarea implicită."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        return response.headers.get(name, default)
    except requests.RequestException:
        return default


def security_headers(url: str) -> dict:
    """Verifică prezența celor cinci antete de securitate cerute."""
    try:
        response = requests.get(url, timeout=TIMEOUT)

        return {
            name: name in response.headers
            for name in SECURITY_HEADERS
        }
    except requests.RequestException:
        return {
            name: False
            for name in SECURITY_HEADERS
        }


def score_headers(results: dict) -> str:
    """Transformă rezultatele într-un scor de forma 3/5."""
    present = sum(bool(value) for value in results.values())
    return f"{present}/{len(results)}"


def fetch_robots(base: str):
    """Returnează textul robots.txt sau None dacă nu este disponibil."""
    try:
        url = base.rstrip("/") + "/robots.txt"
        response = requests.get(url, timeout=TIMEOUT)

        if response.status_code == 200:
            return response.text

        return None
    except requests.RequestException:
        return None


def disallowed_paths(robots_text) -> list:
    """Extrage directivele Disallow din robots.txt; acceptă și None."""
    if not robots_text:
        return []

    paths = []

    for line in robots_text.splitlines():
        line = line.strip()

        if line.lower().startswith("disallow:"):
            value = line.split(":", 1)[1].strip()

            if value:
                paths.append(value)

    return paths


def response_times(*urls: str) -> dict:
    """Returnează timpul de răspuns în secunde pentru fiecare URL."""
    results = {}

    for index, url in enumerate(urls):
        if index:
            time.sleep(1)

        start = time.perf_counter()

        try:
            requests.get(url, timeout=TIMEOUT)
            results[url] = round(time.perf_counter() - start, 4)
        except requests.RequestException:
            results[url] = None

    return results


def log(message: str, **details) -> None:
    """Afișează mesajul și detaliile suplimentare primite ca argumente."""
    extra = " | ".join(
        f"{key}={value}"
        for key, value in details.items()
    )

    print(message + (" | " + extra if extra else ""))


if __name__ == "__main__":
    print("\n-- EXERCIȚIUL 21 -- ")

    try:
        response = fetch(BASE_URL)
        print("Cod de stare:", response.status_code)

        # Exercițiul 22
        print("\n-- EXERCIȚIUL 22 --")
        paths = ["/", "/robots.txt", "/sitemap.xml"]

        for index, path in enumerate(paths):
            if index:
                time.sleep(1)

            url = BASE_URL.rstrip("/") + path
            print(path, "->", get_status(url))

        # Exercițiul 23
        print("\n-- EXERCIȚIUL 23 --")

        try:
            print("Timeout implicit:", fetch(BASE_URL).status_code)
            print("Timeout 3 secunde:", fetch(BASE_URL, timeout=3).status_code)
        except requests.RequestException as error:
            print("Eroare la testarea timeout-ului:", error)

        # Exercițiile 24-25
        print("\n-- EXERCIȚIILE 24-25 --")
        title = get_title(response.text)

        print("Titlu:", title or "(titlu negăsit)")
        print("Docstring:", get_title.__doc__)
        print("Funcția get_title primește HTML și returnează titlul extras.")

        # Exercițiul 26
        print("\n-- EXERCIȚIUL 26 --")
        print(
            "Adnotările de tip nu validează automat "
            "argumentele transmise funcției."
        )

        try:
            print(get_status(123))
        except (requests.RequestException, TypeError, AttributeError) as error:
            print("Apel invalid gestionat:", error)

        # Exercițiul 27
        print("\n-- EXERCIȚIUL 27 --")
        print("Pagina principală există:", page_exists(BASE_URL))
        print(
            "Domeniu inexistent:",
            page_exists("https://this-domain-does-not-exist.invalid")
        )

        # Exercițiul 28
        print("\n-- EXERCIȚIUL 28 --")
        print(check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

        # Exercițiul 29
        print("\n-- EXERCIȚIUL 29 --")
        print("Antet Server:", get_header(BASE_URL, name="Server"))

        # Exercițiile 30-31
        print("\n-- EXERCIȚIILE 30-31 --")
        results = security_headers(BASE_URL)

        print("Antete de securitate:", results)
        print("Scor:", score_headers(results))

        # Exercițiul 32
        print("\n-- EXERCIȚIUL 32 --")
        robots = fetch_robots(BASE_URL)

        print("Căi interzise:", disallowed_paths(robots))
        print("Test cu None:", disallowed_paths(None))

        # Exercițiul 33
        print("\n-- EXERCIȚIUL 33 --")
        print("Timpi de răspuns:", response_times(BASE_URL, ECHO_URL))

        # Exercițiul 34
        print("\n-- EXERCIȚIUL 34 --")
        log(
            "verificat",
            url=BASE_URL,
            status=response.status_code
        )

    except requests.RequestException as error:
        print("Eroare de rețea:", error)

    print(
        "\nVerificare: print() afișează o valoare pe ecran; "
        "return transmite valoarea apelantului pentru reutilizare."
    )