import time
import inspect
import requests
import urllib.request

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


def safe_request():
    """Execută exercițiile care au nevoie de conexiune și tratează erorile."""

    print("\n-- EXERCIȚIUL 1 --")
    print("Versiunea requests:", requests.__version__)
    print("urllib.request a fost importat cu succes.")

    print("\n-- EXERCIȚIUL 2 --")
    try:
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        print("Cu requests.get():", response.status_code)

        from requests import get
        response2 = get(BASE_URL, timeout=TIMEOUT)
        print("Cu from requests import get:", response2.status_code)
    except requests.RequestException as error:
        print("Nu s-a putut accesa site-ul:", error)

    time.sleep(1)

    print("\n-- EXERCIȚIUL 3 --")
    import requests as rq

    try:
        response = rq.get(BASE_URL, timeout=TIMEOUT)
        print("Cod de stare:", response.status_code)
    except rq.RequestException as error:
        print("Eroare de conexiune:", error)

    time.sleep(1)

    print("\n-- EXERCIȚIUL 4 --")
    try:
        request = urllib.request.Request(
            BASE_URL,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; WebLab-Student/1.0)"
            }
        )

        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            body = response.read().decode("utf-8", errors="replace")
            print("Status:", response.status)
            print("Primele 200 de caractere:")
            print(body[:200])

    except urllib.error.HTTPError as error:
        print("Status:", error.code)

        try:
            body = error.read().decode("utf-8", errors="replace")
            print("Primele 200 de caractere ale răspunsului de eroare:")
            print(body[:200] if body else "(serverul nu a trimis corp)")
        except OSError:
            print("Corpul răspunsului nu a putut fi citit.")

        print(
            "Serverul a refuzat cererea urllib. "
            "Aceasta este o restricție a serverului, nu o eroare Python."
        )

    except (urllib.error.URLError, TimeoutError, OSError) as error:
        print("Nu s-a putut accesa site-ul cu urllib:", error)

    print("\n-- EXERCIȚIUL 5 --")
    print("Nume din requests:", dir(requests))
    print("Exemple de categorii:")
    print("get = funcție, Session = clasă, exceptions = modul.")

    print("\n-- EXERCIȚIUL 6 --")
    print("Documentația requests.get, fără pager interactiv:")
    print("Semnătură:", inspect.signature(requests.get))
    print(
        (requests.get.__doc__ or "Documentația nu este disponibilă.")
        .splitlines()[0]
    )
    print("Parametrul pentru timpul maxim de așteptare este timeout.")

    try:
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        print("Cerere cu timeout =", TIMEOUT, "->", response.status_code)
    except requests.RequestException as error:
        print("Cererea a eșuat:", error)

    print("\n-- EXERCIȚIUL 7 --")
    start = time.perf_counter()

    try:
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        elapsed_total = time.perf_counter() - start

        print(
            "Timp total măsurat cu perf_counter():",
            round(elapsed_total, 4),
            "secunde"
        )
        print(
            "response.elapsed:",
            response.elapsed.total_seconds(),
            "secunde"
        )
        print(
            "perf_counter măsoară timpul total din jurul apelului; "
            "response.elapsed măsoară timpul cererii HTTP."
        )
    except requests.RequestException as error:
        print("Cererea a eșuat:", error)

    print("\n-- EXERCIȚIUL 8 --")
    try:
        import bs4
        print("beautifulsoup4 este instalat. Versiune:", bs4.__version__)
    except ImportError:
        print("Instalați modulul cu: python -m pip install beautifulsoup4")


if __name__ == "__main__":
    safe_request()

    print(
        "\nVerificare: modul = fișier Python; "
        "pachet = colecție de module; "
        "bibliotecă = termen general pentru cod reutilizabil."
    )