# Laboratorul 8 — Lucrările A și B

Arhiva conține **două depozite Git locale independente**. Deschide directorul `Laboratorul_8_A_si_B` în Visual Studio Code.

## Lucrarea A — GitHub pas cu pas

În `exercitiu-git` găsești `README.md`, `salut.py`, `.gitignore` și istoric Git cu commituri pentru modificări. În `exercitiu-2` găsești al doilea depozit creat cu `git init`.

Comenzi de verificare în terminalul VS Code (PowerShell):

```powershell
cd exercitiu-git
python salut.py
git status
git log --oneline
git diff
cd ..\exercitiu-2
python exemplu.py
git log --oneline
```

Operațiile A care cer **GitHub** (creare cont, crearea depozitelor publice, `git clone`, `git push`, `git pull`) **nu se pot realiza în numele tău dintr-o arhivă offline**. Pentru a le finaliza, creează cele două depozite publice în contul tău și configurează remote-urile `origin`. Nu folosi `git init` din nou în directoarele din arhivă: au deja `.git`.

Exemplu, după ce creezi un depozit GitHub **gol** cu numele `exercitiu-git` (fără README inițial):

```powershell
cd exercitiu-git
git remote add origin https://github.com/UTILIZATORUL_TAU/exercitiu-git.git
git push -u origin main
```

Pentru `exercitiu-2` se procedează analog. Înlocuiește `UTILIZATORUL_TAU` cu username-ul real. Dacă ai deja un depozit `exercitiu-git` pe GitHub cu istoric propriu, **nu forța un push peste el**; folosește depozitul tău existent și integrează fișierele cu atenție.

## Lucrarea B — Unealta stricată, reparată cu Git

Din directorul `exercitiu-git/depanare`:

```powershell
python inventar.py tinte.json --prag 1000
python inventar.py tinte.json
```

Programul trebuie să afișeze 6 ținte, avertisment pentru portul `abc`, grupurile de servicii, țintele peste prag și mesajul salvării raportului. Raportul `raport_inventar.json` este inclus în arhivă și se regenerează la rulare.

În `exercitiu-git`, `git log --oneline` arată commiturile lucrării A, urmate de commitul inițial al uneltei stricate, **10 commituri de reparații** și commitul raportului.

## Important

Acesta este un proiect demonstrativ complet **local**. Nu pretinde că acțiunile online (crearea depozitelor publice, push/pull) au fost executate. Autorul local al commiturilor este un exemplu și nu reprezintă identitatea ta GitHub. Pentru predare verifică dacă profesorul solicită linkuri către ambele depozite publice.
