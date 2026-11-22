"""Demonstratie pentru fiecare etapa A1-A4 si B1-B4."""
from pathlib import Path
from arsenal.windows.inventar import Proces, Eveniment, Inventar, procese_din_json, evenimente_din_json, construieste_raport

start = Path(__file__).parent / "start"
p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")
print("- A1: Clasa Proces ")
print(p.pid, p.nume)
print(p)
print("- A2: Proces.e_suspect ")
print(p.e_suspect())
print("- A3: Eveniment.e_suspect ")
e = Eveniment(4625, "warning", "Security", "administrator", "An account failed to log on")
print(e.e_suspect(), "-", e.explica())
print("- A4: Citirea JSON ")
procese = procese_din_json(start / "procese.json")
print("procese:", len(procese))
print("suspecte:", sum(p.e_suspect() for p in procese))
print("- B1: Inventar.din_json ")
inv = Inventar.din_json(start / "procese.json")
print("procese:", len(inv))
print("- B2: Interogare ")
for proces in inv.suspecte():
    print(f" [{proces.pid}] {proces.nume} {proces.cale}")
print(inv.pe_user())
print("- B3: Raport ")
ev = evenimente_din_json(start / "evenimente.json")
raport = construieste_raport(inv, ev)
print("Procese:", raport["total_procese"], "| suspecte:", raport["total_procese_suspecte"])
print("Evenimente:", raport["total_evenimente"], "| alarma:", raport["total_alarme"])
print("Scor de risc:", raport["scor_risc"])
print("- B4: Egalitate dataclass ")
print(p == Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe"))
