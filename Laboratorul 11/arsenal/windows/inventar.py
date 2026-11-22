"""Laboratorul 11: obiecte, procese Windows si evenimente de securitate."""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
SUSPECTE_ID = {4625, 1102, 7045}


@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self) -> bool:
        cale = self.cale.replace("/", "\\").lower()
        return any(fragment.lower() in cale for fragment in CAI_SUSPECTE)


@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self) -> bool:
        return self.id in SUSPECTE_ID or self.nivel.lower() == "critical"

    def explica(self) -> str:
        return {4625: "Autentificare esuata (posibil brute force)",
                1102: "Jurnalul de audit a fost sters",
                7045: "A fost instalat un serviciu nou"}.get(
                    self.id, "Eveniment critic" if self.nivel.lower() == "critical" else "Eveniment obisnuit")


def _citeste_lista(cale: str | Path) -> list[dict]:
    with open(cale, encoding="utf-8-sig") as fisier:
        date = json.load(fisier)
    if not isinstance(date, list):
        raise ValueError(f"Fisierul {cale} trebuie sa contina o lista JSON.")
    return date


def procese_din_json(cale: str | Path) -> list[Proces]:
    return [Proces(**d) for d in _citeste_lista(cale)]


def evenimente_din_json(cale: str | Path) -> list[Eveniment]:
    return [Eveniment(**d) for d in _citeste_lista(cale)]


@dataclass
class Inventar:
    procese: list[Proces]

    @classmethod
    def din_json(cls, cale: str | Path) -> Inventar:
        return cls(procese_din_json(cale))

    def __len__(self) -> int:
        return len(self.procese)

    def suspecte(self) -> list[Proces]:
        return [p for p in self.procese if p.e_suspect()]

    def pe_user(self) -> dict[str, list[str]]:
        rezultat: dict[str, list[str]] = {}
        for proces in self.procese:
            rezultat.setdefault(proces.user, []).append(proces.nume)
        return rezultat

    def scor(self, evenimente: list[Eveniment] | None = None) -> int:
        return len(self.suspecte()) + sum(e.e_suspect() for e in (evenimente or []))


def construieste_raport(inventar: Inventar, evenimente: list[Eveniment]) -> dict:
    alarme = [e for e in evenimente if e.e_suspect()]
    return {
        "total_procese": len(inventar),
        "total_procese_suspecte": len(inventar.suspecte()),
        "procese_suspecte": [asdict(p) for p in inventar.suspecte()],
        "procese_pe_utilizator": inventar.pe_user(),
        "total_evenimente": len(evenimente),
        "total_alarme": len(alarme),
        "alarme": [asdict(e) for e in alarme],
        "scor_risc": inventar.scor(evenimente),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventar de procese si evenimente Windows")
    parser.add_argument("capturi", type=Path, help="Folder cu procese.json si evenimente.json")
    parser.add_argument("--json", action="store_true", help="Afiseaza raportul JSON")
    parser.add_argument("--salveaza", type=Path, help="Salveaza raportul JSON intr-un fisier")
    args = parser.parse_args()
    try:
        inventar = Inventar.din_json(args.capturi / "procese.json")
        evenimente = evenimente_din_json(args.capturi / "evenimente.json")
        raport = construieste_raport(inventar, evenimente)
        if args.salveaza:
            args.salveaza.parent.mkdir(parents=True, exist_ok=True)
            args.salveaza.write_text(json.dumps(raport, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if args.json:
            print(json.dumps(raport, indent=2, ensure_ascii=False))
        else:
            print(f"Procese: {len(inventar)} | suspecte: {len(inventar.suspecte())}")
            for proces in inventar.suspecte():
                print(f" [{proces.pid}] {proces.nume} ({proces.user}) {proces.cale}")
            alarme = [e for e in evenimente if e.e_suspect()]
            print(f"Evenimente: {len(evenimente)} | alarma: {len(alarme)}")
            for eveniment in alarme:
                print(f" {eveniment.id} [{eveniment.nivel}] {eveniment.cont}: {eveniment.mesaj}")
            print(f"Scor de risc: {inventar.scor(evenimente)}")
            if args.salveaza:
                print(f"Raport salvat: {args.salveaza}")
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as eroare:
        parser.exit(1, f"Eroare la citirea capturilor: {eroare}\n")


if __name__ == "__main__":
    main()
