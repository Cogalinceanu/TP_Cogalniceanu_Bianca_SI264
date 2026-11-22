"""Lucrarea A: extragerea si numararea esecurilor SSH."""
import argparse
import re
from collections import Counter

TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")


def esec(linie):
    """Intoarce (utilizator, IP) pentru un esec SSH, altfel None."""
    m = TIPAR.search(linie)
    if m is None:
        return None
    return (m.group(1), m.group(2))


def citeste_esecuri(cale):
    """Intoarce lista de dict-uri; un fisier absent produce lista vida."""
    esecuri = []
    try:
        with open(cale, encoding="utf-8") as fisier:
            for linie in fisier:
                rezultat = esec(linie)
                if rezultat is not None:
                    esecuri.append({"user": rezultat[0], "ip": rezultat[1]})
    except FileNotFoundError:
        print("nu gasesc", cale)
    except (PermissionError, IsADirectoryError, UnicodeError, OSError) as eroare:
        print(f"nu pot citi {cale}: {eroare}")
    return esecuri


def pe_ip(esecuri):
    """Intoarce un Counter cu numarul de esecuri pentru fiecare IP."""
    return Counter(e["ip"] for e in esecuri)


def main():
    parser = argparse.ArgumentParser(description="Analiza esecurilor SSH din auth.log")
    parser.add_argument("log", help="Calea catre jurnalul SSH")
    args = parser.parse_args()
    esecuri = citeste_esecuri(args.log)
    print(f"Esecuri de autentificare: {len(esecuri)}")
    for ip, numar in pe_ip(esecuri).most_common():
        print(f" {ip}: {numar}")


if __name__ == "__main__":
    main()
