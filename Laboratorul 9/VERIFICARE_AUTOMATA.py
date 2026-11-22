"""Verificare offline, fara biblioteci externe."""
from pathlib import Path
import json
from arsenal.privesc.enum import citeste_linii, enumereaza, utilizatori_implicati
from arsenal.privesc.diferenta import compara

start = Path(__file__).parent / "arsenal" / "privesc" / "start"
raport = enumereaza(start)
baza, acum, noi, risc, periculoase = compara(start / "baza_suid.txt", start / "suid.txt")
verificari = {
    "A1: 14 linii SUID": len(citeste_linii(start / "suid.txt")) == 14,
    "A2-A3: 13 unice, 4 risc mare": len(raport["suid"]) == 13 and sum(x["risc"] == "mare" for x in raport["suid"]) == 4,
    "A4: sudo si cron": len(raport["sudo"]) == 3 and len(raport["cron"]) == 3,
    "A5: utilizatori si JSON": utilizatori_implicati(raport) == {"ana", "root", "www-data"} and isinstance(json.loads(json.dumps(raport)), dict),
    "B1-B3: baza, acum, noi si periculoase": (len(baza), len(acum), len(noi), len(periculoase)) == (9, 13, 4, 4),
}
for nume, ok in verificari.items():
    print(("[OK] " if ok else "[EROARE] ") + nume)
print(f"Rezultat: {sum(verificari.values())} / {len(verificari)} verificari reusite")
raise SystemExit(0 if all(verificari.values()) else 1)
