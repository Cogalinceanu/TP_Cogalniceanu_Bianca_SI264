import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


def main():
    """Demonstrează atributele și metodele obiectelor Response."""

    try:
        response = requests.get(BASE_URL, timeout=TIMEOUT)

        print("\n= EXERCIȚIUL 9 =====")
        print("status_code (atribut):", response.status_code)
        print("ok (atribut):", response.ok)
        print("url (atribut):", response.url)
        print("encoding (atribut):", response.encoding)

        print("\n-- EXERCIȚIUL 10")

        try:
            response.raise_for_status()
            print("Pagina principală a răspuns fără eroare HTTP.")
        except requests.HTTPError as error:
            print("Pagina principală a returnat o eroare HTTP:", error)

        time.sleep(1)

        try:
            missing = requests.get(
                BASE_URL + "/this-page-does-not-exist",
                timeout=TIMEOUT
            )
            missing.raise_for_status()
            print("Pagina de test a răspuns fără eroare HTTP.")
        except requests.HTTPError:
            print(
                "Pagina de test nu a fost găsită "
                "sau serverul a returnat o eroare HTTP."
            )
        except requests.RequestException as error:
            print("Eroare de rețea la pagina de test:", error)

        print("\n-- EXERCIȚIUL 11 --")
        for name, value in response.headers.items():
            print(f"{name}: {value}")

        print("\n-- EXERCIȚIUL 12 --")
        print("Server:", response.headers.get("Server", "lipsește"))
        print(
            "Content-Type:",
            response.headers.get("Content-Type", "lipsește")
        )
        print(
            "content-type cu litere mici:",
            response.headers.get("content-type", "lipsește")
        )
        print(
            "requests permite accesarea antetelor fără "
            "a ține cont de majuscule/minuscule."
        )

        print("\n-- EXERCIȚIUL 13 --")
        print(
            'Numărul aparițiilor cuvântului "cyber":',
            response.text.lower().count("cyber")
        )

        print("\n-- EXERCIȚIUL 14 --")
        html = response.text
        lower_html = html.lower()

        start = lower_html.find("<title>")
        end = lower_html.find("</title>")

        if start != -1 and end != -1 and end >= start:
            title = html[start + len("<title>"):end].strip()
            print("Titlu:", title)
        else:
            print("Titlul nu a fost găsit în HTML.")

        print("\n-- EXERCIȚIUL 15 --")
        lines = response.text.splitlines()
        print("Număr de linii:", len(lines))

        longest_line = max((len(line) for line in lines), default=0)
        print("Lungimea celei mai lungi linii:", longest_line)

        print("\n-- EXERCIȚIUL 16 --")
        if response.url.startswith("https://"):
            print("Conexiune HTTPS.")
        else:
            print("Conexiune fără HTTPS.")

        print("\n-- EXERCIȚIUL 17 --")
        time.sleep(1)

        try:
            redirect_response = requests.get(
                "http://cybercor.org",
                timeout=TIMEOUT,
                allow_redirects=True
            )

            if redirect_response.history:
                for item in redirect_response.history:
                    print(
                        item.status_code,
                        item.url,
                        "->",
                        item.headers.get("Location", "(fără Location)")
                    )
            else:
                print("Nu au fost raportate redirecționări.")

            print("URL final:", redirect_response.url)

        except requests.RequestException as error:
            print("Nu s-au putut verifica redirecționările:", error)

        print("\n-- EXERCIȚIUL 18 --")
        time.sleep(1)

        try:
            head_response = requests.head(
                BASE_URL,
                timeout=TIMEOUT,
                allow_redirects=True
            )
            get_response = requests.get(BASE_URL, timeout=TIMEOUT)

            print("Cod HEAD:", head_response.status_code)
            print("Lungime corp HEAD:", len(head_response.content))
            print("Cod GET:", get_response.status_code)
            print("Lungime corp GET:", len(get_response.content))
            print(
                "HEAD returnează de regulă antete fără corp; "
                "GET descarcă și corpul paginii."
            )
        except requests.RequestException as error:
            print("Eroare la compararea HEAD și GET:", error)

        print("\n-- EXERCIȚIUL 19 --")

        if response.cookies:
            for cookie in response.cookies:
                print("Nume:", cookie.name, "| Secure:", cookie.secure)
        else:
            print("Niciun cookie setat în răspuns.")

        print("\n-- EXERCIȚIUL 20 --")

        try:
            with requests.Session() as session:
                session.headers.update({"User-Agent": "WebLab-Student"})

                time.sleep(1)
                echo_response = session.get(
                    ECHO_URL + "/headers",
                    timeout=TIMEOUT
                )
                echo_response.raise_for_status()

                data = echo_response.json()
                received = data.get("headers", {}).get("User-Agent", "")

                print("User-Agent trimis:", received)
                print(
                    "Antet confirmat:",
                    "WebLab-Student" in received
                )

        except requests.RequestException as error:
            print("Nu s-a putut verifica User-Agent:", error)
        except ValueError as error:
            print("Răspunsul serverului nu este JSON valid:", error)

    except requests.RequestException as error:
        print("Eroare la accesarea site-ului:", error)

    print(
        "\nVerificare: response.text este un atribut cu textul corpului; "
        "response.json() este o metodă care interpretează corpul ca JSON."
    )


if __name__ == "__main__":
    main()