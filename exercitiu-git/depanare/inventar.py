import argparse
import json


def citeste_tinte(fisier):
    """Citeste tintele din fisierul JSON."""
    with open(fisier, "r", encoding="utf-8") as f:
        date = json.load(f)

    return date["tinte"]


def verifica_port(port):
    """Intoarce portul ca numar daca este valid, altfel None."""
    try:
        port = int(port)
    except (ValueError, TypeError):
        return None

    if 1 <= port <= 65535:
        return port

    return None


def clasifica_port(port):
    """Asociaza porturile cunoscute cu serviciile lor."""
    servicii = {
        22: "ssh",
        80: "http",
        8080: "http",
        3306: "mysql",
    }
    return servicii.get(port, "necunoscut")


def analizeaza_tinte(tinte, prag):
    servicii = {}
    peste_prag = []

    for tinta in tinte:
        ip = tinta.get("ip", "IP necunoscut")
        scor = tinta.get("scor", 0)

        if scor > prag:
            peste_prag.append(ip)

        for port_initial in tinta.get("porturi", []):
            port = verifica_port(port_initial)

            if port is None:
                print(f"sar peste {ip} : port invalid {port_initial}")
                continue

            serviciu = clasifica_port(port)
            if serviciu not in servicii:
                servicii[serviciu] = []

            if port not in servicii[serviciu]:
                servicii[serviciu].append(port)

    return servicii, peste_prag


def salveaza_raport(servicii, peste_prag):
    raport = {
        "servicii": servicii,
        "peste_prag": peste_prag,
    }

    with open("raport_inventar.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=4, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Analiza inventarului de porturi"
    )
    parser.add_argument("fisier", help="Fisierul JSON cu tintele")
    parser.add_argument(
        "--prag",
        type=int,
        default=1024,
        help="Pragul pentru selectarea tintelor (implicit: 1024)",
    )
    args = parser.parse_args()

    tinte = citeste_tinte(args.fisier)
    print(f"Tinte citite: {len(tinte)}")

    servicii, peste_prag = analizeaza_tinte(tinte, args.prag)

    for serviciu, porturi in servicii.items():
        print(f"{serviciu}: {porturi}")

    print(f"Peste {args.prag}: {peste_prag}")

    salveaza_raport(servicii, peste_prag)
    print("Raport salvat in raport_inventar.json")


if __name__ == "__main__":
    main()
