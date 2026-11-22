"""Laboratorul 9, lucrarea A: colectii si raport JSON din capturi Linux."""
import argparse
import json
import os

GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash", "less", "awk", "python3", "perl"}


def citeste_linii(cale):
    """Lista liniilor ne-goale, fara comentarii, pastrand ordinea si dublurile."""
    with open(cale, encoding="utf-8") as f:
        return [linie.strip() for linie in f if linie.strip() and not linie.strip().startswith("#")]


def nume(cale):
    """Ultima componenta dintr-o cale Unix."""
    return cale.rsplit("/", 1)[-1]


def suid_constatari(cale):
    """O constatare pentru fiecare cale SUID unica, sortata."""
    return [{"cale": c, "nume": nume(c), "risc": "mare" if nume(c) in GTFO else "normal"}
            for c in sorted(set(citeste_linii(cale)))]


def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)  # despachetarea tuplului
        out.append({"user": user.strip(), "drept": drept.strip(),
                    "risc": "mare" if "NOPASSWD" in drept else "normal"})
    return out


def cron_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        if len(campuri) < 7:
            raise ValueError(f"Linie cron invalida: {ln!r}")
        # Format crontab de sistem: 5 campuri de timp, apoi user si comanda.
        user = campuri[5]
        comanda = " ".join(campuri[6:])
        out.append({"user": user, "comanda": comanda})
    return out


def enumereaza(d):
    return {"suid": suid_constatari(os.path.join(d, "suid.txt")),
            "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
            "cron": cron_constatari(os.path.join(d, "crontab.txt"))}


def utilizatori_implicati(raport):
    return {c["user"] for c in raport["sudo"]} | {c["user"] for c in raport["cron"]}


def grupare_dupa_risc(raport):
    grupuri = {}
    for categorie, constatari in raport.items():
        for c in constatari:
            grupuri.setdefault(c.get("risc", "normal"), []).append(c.get("nume", c.get("user", "necunoscut")))
    return grupuri


def main(argv=None):
    p = argparse.ArgumentParser(description="Enumerare SUID, sudo si cron din capturi")
    p.add_argument("capturi", help="Directorul cu suid.txt, sudo.txt, crontab.txt")
    p.add_argument("--json", action="store_true", help="Afiseaza exclusiv JSON pe stdout")
    p.add_argument("--risc", choices=["mare", "normal"], help="Filtreaza constatarile dupa risc")
    p.add_argument("--grupare-risc", action="store_true", help="Afiseaza gruparea dupa risc")
    a = p.parse_args(argv)
    raport = enumereaza(a.capturi)
    if a.risc:
        raport = {categorie: [c for c in lista if c.get("risc", "normal") == a.risc]
                  for categorie, lista in raport.items()}
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")
    print("utilizatori implicati:", ", ".join(sorted(utilizatori_implicati(raport))))
    if a.grupare_risc:
        print("grupare dupa risc:", json.dumps(grupare_dupa_risc(raport), ensure_ascii=False))
    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")


if __name__ == "__main__":
    main()
