# Laboratorul 9 – Colecții în Python

**UTM · Tehnici de programare · Lucrarea A și Lucrarea B**

Proiectul folosește exclusiv capturile din `start.zip`. Nu scanează un sistem real și nu necesită conexiune la internet pentru rularea programelor.

## Cum deschizi proiectul

1. Dezarhivează `Laboratorul_9.zip`.
2. Deschide **VS Code → File → Open Folder → Laboratorul_9**.
3. Deschide terminalul din VS Code (**Terminal → New Terminal**). Toate comenzile de mai jos se execută din folderul `Laboratorul_9`, nu din `arsenal/privesc`.

## Lucrarea A

```powershell
python -m arsenal.privesc.enum arsenal/privesc/start
```

Rezultat așteptat:

```text
suid: 13 gasite, 4 cu risc mare
sudo: 3 gasite, 2 cu risc mare
cron: 3 gasite, 0 cu risc mare
utilizatori implicati: ana, root, www-data
Raport salvat in enum.json
```

Raportul apare la rădăcină (`enum.json`); o copie a raportului inițial este deja inclusă și în `arsenal/privesc/enum.json` pentru predare.

Pentru afișarea exclusivă a JSON-ului:

```powershell
python -m arsenal.privesc.enum arsenal/privesc/start --json
```

## Lucrarea B

```powershell
python -m arsenal.privesc.diferenta
```

Rezultat așteptat: `baza: 9 acum: 13`, 4 fișiere noi și 4 fișiere noi periculoase: `/bin/cp`, `/usr/bin/find`, `/usr/bin/nmap`, `/usr/bin/vim.basic`.

## Testare

Instalează pytest dacă nu îl ai deja:

```powershell
python -m pip install pytest
```

Rulează testul cerut de fișă:

```powershell
python -m pytest -q arsenal/privesc/test_diferenta.py
```

Fișierul conține testul minim B4 plus verificări suplimentare pentru toate etapele. Poți verifica și proiectul fără pytest prin `python VERIFICARE_AUTOMATA.py`.

## Opțional: filtrare și grupare

```powershell
python -m arsenal.privesc.enum arsenal/privesc/start --json --risc mare
python -m arsenal.privesc.enum arsenal/privesc/start --grupare-risc
```

Opțiunea de scanare directă a unui sistem Linux real nu este activată: pentru acest laborator sunt suficiente capturile furnizate, iar scanarea unei ținte necesită autorizare.

## Colecții utilizate

- **Listă:** liniile din capturi și constatările, păstrează ordinea.
- **Tuplu:** despachetarea `user, drept` la sudo.
- **Mulțime:** elimină dublurile, reunește utilizatorii și calculează diferența dintre sisteme.
- **Dicționar:** descrie fiecare constatare, grupează raportul și riscurile.
- **Comprehensions:** creează mulțimi, liste și dicționare concise.

## Predare prin Git

Din rădăcina propriului depozit de curs, copiază folderul `arsenal/privesc`, apoi rulează:

```powershell
git add arsenal/privesc
git commit -m "privesc: enum SUID/sudo/cron -> JSON, diferenta fata de baza"
git push
```

Comenzile Git funcționează numai într-un depozit Git configurat; arhiva de față nu conține `.git` și nu efectuează automat un push.
