"""Laboratorul 9, lucrarea B: diferenta SUID fata de baza curata."""
import argparse
from arsenal.privesc.enum import citeste_linii, nume, GTFO


def cai(fisier):
    return set(citeste_linii(fisier))


def compara(fisier_baza, fisier_acum):
    baza = cai(fisier_baza)
    acum = cai(fisier_acum)
    noi = acum - baza
    risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}
    periculoase = [c for c in sorted(noi) if nume(c) in GTFO]
    return baza, acum, noi, risc, periculoase


def main(argv=None):
    p = argparse.ArgumentParser(description="Compara doua liste SUID")
    p.add_argument("--baza", default="arsenal/privesc/start/baza_suid.txt")
    p.add_argument("--acum", default="arsenal/privesc/start/suid.txt")
    a = p.parse_args(argv)
    baza, acum, noi, risc, periculoase = compara(a.baza, a.acum)
    print("baza:", len(baza), "acum:", len(acum))
    print(len(noi), "SUID noi fata de sistemul curat")
    for c in sorted(noi):
        print(" ", c)
    print("risc:", dict(sorted(risc.items())))
    print("periculoase NOI:", periculoase)


if __name__ == "__main__":
    main()
