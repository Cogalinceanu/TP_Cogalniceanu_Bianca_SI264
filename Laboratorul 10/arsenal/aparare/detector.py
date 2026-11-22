"""Lucrarea B: detector de brute force si raport JSON."""
import argparse
import json
from arsenal.aparare.parse_auth import citeste_esecuri, pe_ip


def suspecti(counts, prag=10):
    """Intoarce (IP, numar) pentru IP-urile cu cel putin prag esecuri."""
    if not isinstance(prag, int) or isinstance(prag, bool) or prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    return sorted(((ip, n) for ip, n in counts.items() if n >= prag),
                  key=lambda element: (-element[1], element[0]))


def genereaza_raport(esecuri, prag=10):
    """Construieste un raport serializabil JSON, fara afisare."""
    counts = pe_ip(esecuri)
    return {
        "esecuri": len(esecuri),
        "pe_ip": dict(counts.most_common()),
        "suspecti": [{"ip": ip, "incercari": n} for ip, n in suspecti(counts, prag)],
    }


def main():
    parser = argparse.ArgumentParser(description="Detecteaza incercari brute force SSH")
    parser.add_argument("log", help="Calea catre auth.log")
    parser.add_argument("--prag", type=int, default=10, help="Numarul minim de esecuri (implicit 10)")
    parser.add_argument("--json", action="store_true", help="Afiseaza un raport JSON")
    args = parser.parse_args()
    try:
        # Validare inainte de citirea fisierului, inclusiv pentru fisiere inexistente.
        suspecti({}, args.prag)
    except ValueError as eroare:
        parser.error(str(eroare))
    esecuri = citeste_esecuri(args.log)
    raport = genereaza_raport(esecuri, args.prag)
    if args.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
    else:
        print(f"Esecuri de autentificare: {raport['esecuri']}")
        for ip, n in raport["pe_ip"].items():
            print(f" {ip}: {n}")
        print(f"Suspecti (prag {args.prag}):")
        for item in raport["suspecti"]:
            print(f" {item['ip']} ({item['incercari']} incercari) BRUTE FORCE")


if __name__ == "__main__":
    main()
