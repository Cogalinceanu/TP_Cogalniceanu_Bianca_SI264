# Laboratorul 11 – Obiecte și clase

**Tema:** Windows în Python: inventar de procese și jurnalul de evenimente.

Sunt rezolvate integral lucrările A1–A4 și B1–B4, plus metodele opționale `explica()` și `scor()`. Capturile JSON originale din arhiva de start sunt incluse.

## Cum rulezi (Windows, PowerShell / terminal VS Code)

1. Dezarhivează `Laboratorul_11.zip` și deschide **folderul Laboratorul_11** în VS Code.
2. Deschide terminalul în rădăcina folderului (acolo unde se află `arsenal`).
3. Rulează comenzile de mai jos, pe rând:

```powershell
python -m arsenal.windows.inventar arsenal/windows/start
python -m arsenal.windows.inventar arsenal/windows/start --json
python -m arsenal.windows.inventar arsenal/windows/start --salveaza raport_alarme.json
python -m arsenal.windows.demo_etape
python -m pytest -q arsenal/windows/test_inventar.py
```

Pentru teste, dacă nu ai pytest: `python -m pip install pytest`.

## Rezultate așteptate

- 7 procese, dintre care 2 suspecte (PID 3120 și 3890).
- 8 evenimente, dintre care 5 alarme.
- Scor de risc: 7 (numărul de procese suspecte + evenimente de alarmă).
- Fișierul `raport_alarme.json` este creat la comanda cu `--salveaza`.

## Structură

- `arsenal/windows/inventar.py`: clase, metode, citire JSON, CLI, raport.
- `arsenal/windows/demo_etape.py`: demonstrații A1–A4, B1–B4.
- `arsenal/windows/test_inventar.py`: teste automate pytest.
- `arsenal/windows/start/`: datele originale primite la laborator.
- `raport_alarme.json`: raport exemplu generat din capturi.

## Predare Git

Din rădăcina depozitului tău Git, copiază folderul `arsenal/windows` din acest proiect, apoi:

```powershell
git add arsenal/windows
git commit -m "windows: inventar procese + jurnal ca obiecte, in Python"
git push
```

Nu rula `git init` într-un depozit Git deja existent.

**Notă:** citirea capturilor de pe laptopul propriu necesită un export adaptat la câmpurile `pid`, `nume`, `user`, `cale`; `Get-Process | ConvertTo-Json` în forma brută nu produce automat această schemă.
