import argparse
import json


def citeste_tinte(cale):
    with open(cale, "r", encoding="utf-8") as fisier:
        date = json.load(fisier)
    return date["tinte"]


def grupeaza(tinte):
    grupuri = {}
    erori = []
    for tinta in tinte:
        serviciu = tinta.get("serviciu", "necunoscut")
        try:
            port = int(tinta["port"])
        except (ValueError, TypeError):
            erori.append(f"sar peste {tinta.get('ip', 'necunoscut')} : port invalid {tinta.get('port')}")
            continue
        grupuri.setdefault(serviciu, []).append(port)
    return grupuri, erori


def peste_prag(tinte, prag):
    rezultat = []
    for tinta in tinte:
        if int(tinta["valoare"]) > prag:
            rezultat.append(tinta["ip"])
    return rezultat


def construieste_raport(tinte, grupuri, peste, prag):
    raport = {
        "total_tinte": len(tinte),
        "prag": prag,
        "servicii": grupuri,
        "peste_prag": peste
    }
    return raport


def main():
    parser = argparse.ArgumentParser(description="Inventariaza tinte si porturi.")
    parser.add_argument("fisier", help="Fisier JSON cu lista de tinte")
    parser.add_argument("--prag", type=int, default=1024, help="Pragul pentru filtrare")
    args = parser.parse_args()

    tinte = citeste_tinte(args.fisier)
    print("Tinte citite: " + str(len(tinte)))

    grupuri, erori = grupeaza(tinte)
    for eroare in erori:
        print(eroare)
    for serviciu, porturi in grupuri.items():
        print(f"{serviciu}: {porturi}")

    peste = peste_prag(tinte, args.prag)
    print(f"Peste {args.prag}: {peste}")

    raport = construieste_raport(tinte, grupuri, peste, args.prag)
    with open("raport_inventar.json", "w", encoding="utf-8") as fisier:
        json.dump(raport, fisier, indent=4, ensure_ascii=False)
    print("Raport salvat in raport_inventar.json")


if __name__ == "__main__":
    main()
