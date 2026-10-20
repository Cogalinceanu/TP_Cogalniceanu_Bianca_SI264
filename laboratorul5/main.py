import argparse
import csv
from datetime import datetime

from webtools import (
    DEFAULT_HEADERS,
    check_paths,
    fetch,
    get_title,
    security_headers,
    site_report,
)


def save_csv_report(
    base_url: str,
    filename: str = "report.csv"
) -> dict:
    """Salvează codurile HTTP pentru căile standard într-un fișier CSV."""

    paths = [
        "/",
        "/robots.txt",
        "/sitemap.xml",
    ]

    results = check_paths(base_url, paths)
    checked_at = datetime.now().isoformat()

    try:
        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.writer(file)

            writer.writerow([
                "path",
                "status",
                "checked_at"
            ])

            for path, status in results.items():
                writer.writerow([
                    path,
                    status,
                    checked_at
                ])

        print(f"Raportul CSV a fost salvat în {filename}")

    except OSError as error:
        print("Nu s-a putut salva raportul CSV:", error)

    return results


def main():
    """Citește URL-ul și rulează raportul site-ului."""

    parser = argparse.ArgumentParser(
        description="Generează un raport simplu despre un site web."
    )

    parser.add_argument(
        "url",
        nargs="?",
        default="https://cybercor.org",
        help=(
            "URL-ul care va fi analizat "
            "(implicit: https://cybercor.org)"
        ),
    )

    args = parser.parse_args()
    url = args.url

    print("Antete implicite:", DEFAULT_HEADERS)

    # Exercițiile 44-45: importuri din modulul propriu
    print("\n-- EXERCIȚIILE 44-45 --")

    try:
        response = fetch(url)

        print(
            "Cod de stare:",
            response.status_code
        )

        print(
            "Titlul paginii:",
            get_title(response.text) or "(titlu negăsit)"
        )

        print(
            "Antete de securitate:",
            security_headers(url)
        )

    except Exception as error:
        print(
            "Nu s-a putut obține pagina pentru exemplele de import:",
            error
        )

    # Exercițiul 46: comportamentul __name__
    print("\n-- EXERCIȚIUL 46 --")
    print(
        "Funcțiile importate din webtools.py sunt reutilizate "
        "fără a executa blocul său principal."
    )
    print(
        "Blocul if __name__ == '__main__' rulează doar "
        "când fișierul respectiv este pornit direct."
    )

    # Exercițiile 47-48: folosirea funcțiilor importate
    print("\n-- EXERCIȚIILE 47-48 --")

    try:
        print(
            "Status pentru URL:",
            fetch(url).status_code
        )

        print(
            "Antete de securitate:",
            security_headers(url)
        )

    except Exception as error:
        print("Eroare la exercițiile 47-48:", error)

    print("\n-- EXERCIȚIUL 49 --")

    try:
        csv_results = save_csv_report(url)
        print("Rezultatele CSV:", csv_results)

    except Exception as error:
        print("Nu s-a putut genera raportul CSV:", error)

    print("\n-- EXERCIȚIUL 50 --")

    try:
        site_report(url, "report.json")

    except Exception as error:
        print("Nu s-a putut genera raportul JSON:", error)


if __name__ == "__main__":
    main()