import requests

SITES = [

    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",

    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",

    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",

    "https://httpbin.org/status/200,500",
]


SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă."""
    path = path.lstrip("/")
    return "https://" + host.rstrip("/") + "/" + path if path else "https://" + host.rstrip("/")


def is_https(url):
    """Verifică dacă adresa începe cu https://."""
    return url.lower().startswith("https://")


def show_response(url):
    """Trimite un GET și afișează statusul și Content-Type."""
    try:
        response = requests.get(url, timeout=5)
        print("Status:", response.status_code)
        print("Content-Type:", response.headers.get("Content-Type", "unknown"))
    except requests.RequestException as error:
        print("Eroare:", str(error))


def check_site(url):
    """Returnează informații despre site într-un dicționar."""
    try:
        response = requests.get(url, timeout=5)

        content_type = response.headers.get("Content-Type", "unknown")
        content_type = content_type.split(";")[0].strip()

        return {
            "status": response.status_code,
            "content_type": content_type,
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown")
        }

    except requests.RequestException as error:
        return {
            "status": None,
            "error": str(error)
        }


def scan_sites():
    """Verifică site-urile, afișează rezultatele și rezumatul."""
    results = []

    for url in SITES:
        result = check_site(url)
        result["url"] = url
        results.append(result)

    working = [
        result for result in results
        if result.get("status") == 200
    ]

    working.sort(
        key=lambda result: result.get("length", 0),
        reverse=True
    )

    print("\n SITE-URI FUNCȚIONALE")

    for result in working:
        print(
            result["url"],
            "->",
            result["status"],
            ",",
            result["length"],
            "octeți"
        )

    failed = len(results) - len(working)

    print("\n REZUMAT")
    print("Reușite:", len(working), "| Eșuate:", failed)

    return results


def check_headers(url):
    """Verifică antetele de securitate și calculează scorul."""
    try:
        response = requests.get(url, timeout=5)

        received_headers = {
            header.lower()
            for header in response.headers
        }

        present = []
        missing = []

        for header in SECURITY_HEADERS:
            if header.lower() in received_headers:
                present.append(header)
            else:
                missing.append(header)

        score = int(
            len(present) / len(SECURITY_HEADERS) * 100
        )

        return {
            "present": present,
            "missing": missing,
            "score": score
        }

    except requests.RequestException as error:
        return {
            "status": None,
            "error": str(error)
        }


def retry_check(url, attempts=3):
    """Reîncearcă cererea dacă apare o eroare sau un status 5xx."""

    if attempts < 1:
        return {
            "status": None,
            "error": "Numărul de încercări trebuie să fie cel puțin 1",
            "attempts": 0
        }

    status = None
    last_error = None
    actual_attempts = 0

    for i in range(attempts):
        actual_attempts += 1

        try:
            response = requests.get(url, timeout=5)
            status = response.status_code
            last_error = None

            if status < 500:
                return {
                    "status": status,
                    "attempts": actual_attempts
                }

        except requests.RequestException as error:
            status = None
            last_error = str(error)

    result = {
        "status": status,
        "attempts": actual_attempts
    }

    if status is None and last_error is not None:
        result["error"] = last_error

    return result