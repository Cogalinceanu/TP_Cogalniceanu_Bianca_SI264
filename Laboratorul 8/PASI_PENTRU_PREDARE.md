# Laboratorul 8 — verificare și predare (Lucrarea A + Lucrarea B)

## 1. Verificarea locală automată

Deschide folderul `Laboratorul_8_A_si_B` în VS Code. În terminal:

```powershell
python VERIFICARE_AUTOMATA.py
```

Trebuie să vezi `4 / 4 verificari locale reusite`. Scriptul verifică cele două programe din Lucrarea A, istoricul Git local și ieșirea + raportul din Lucrarea B. **Nu verifică operațiile online GitHub.**

## 2. Lucrarea A — ce poți verifica în arhivă

În `exercitiu-git` există `README.md`, `salut.py`, `.gitignore` și mai multe commituri locale. În `exercitiu-2` există `README.md`, `exemplu.py` și istoric Git separat. Din terminal:

```powershell
cd exercitiu-git
python salut.py
git log --oneline
git status
cd ..\exercitiu-2
python exemplu.py
git log --oneline
```

### Ce trebuie făcut efectiv în contul tău pentru A1–A11

- **A1–A2:** verifică autentificarea GitHub și configurează Git cu numele și e-mailul tău real (`git config --global user.name`, `git config --global user.email`). Identitatea demonstrativă din commiturile arhivei nu este identitatea ta.
- **A3–A4:** fișa cere crearea unui depozit public `exercitiu-git` cu README pe GitHub și **clonarea** lui. Arhiva conține în schimb un depozit local demonstrativ, deci operația `git clone` trebuie demonstrată separat în contul tău. Dacă ai deja un depozit creat, nu îl suprascrie.
- **A5–A6:** rulează `salut.py`, apoi verifică `git status`, `git add`, `git commit` și `git push` pe propriul depozit. Fișierele deja comise în arhivă nu apar ca „untracked”. Pentru demonstrația A5, fă o schimbare nouă și salveaz-o.
- **A7:** modifică `README.md` direct pe GitHub, apasă Commit changes, apoi execută `git pull` în depozitul local conectat și verifică noul rând.
- **A8:** `.gitignore` din arhivă exclude `.venv/` și `__pycache__/`. Poți verifica prin `python -m venv .venv` și `git status --short`.
- **A9:** rulează `git log --oneline`; modifică temporar `salut.py`, rulează `git diff`, apoi `git restore salut.py` ca în fișă.
- **A10:** fișa cere al doilea depozit `exercitiu-2` creat local cu `git init`, apoi conectat și publicat pe GitHub. Arhiva conține deja exemplul local; publicarea rămâne de făcut.
- **A11:** verifică în browser că ambele depozite sunt **Public**, că `exercitiu-git` conține `README.md`, `salut.py`, `.gitignore` și cel puțin 4 commituri și că `exercitiu-2` conține `README.md`.

**Important despre încărcare:** dacă pe GitHub există deja `exercitiu-git` cu propriul istoric, nu rula `git push --force` și nu încerca să înlocuiești istoricul. Integrează fișierele în depozitul tău existent. Dacă depozitele GitHub sunt goale, poți conecta fiecare depozit local cu `git remote add origin https://github.com/UTILIZATORUL_TAU/NUMELE_DEPOZITULUI.git` și apoi `git push -u origin main`.

## 3. Lucrarea B — verificare

```powershell
cd exercitiu-git\depanare
python inventar.py tinte.json --prag 1000
python inventar.py tinte.json
python inventar.py tinte.json --prag 1000
cd ..
git log --oneline
```

A doua comandă folosește pragul implicit `1024`. A treia reface raportul cu pragul `1000` pentru predare. Istoricul local conține un commit inițial cu unealta stricată, 10 commituri distincte de reparare și commitul raportului.

## 4. Ce se predă

Conform fișei A: **linkurile celor două depozite publice GitHub**, nu doar arhiva ZIP. Pentru Lucrarea B trebuie să poți demonstra rularea și istoricul celor 10 reparații. Arhiva este un exemplu local, nu o dovadă că ai efectuat tu operațiile online în contul personal.
