LABORATORUL 8 - LUCRARILE A SI B
Pachet pregatit pentru executare pe Windows / PowerShell.

IMPORTANT:
1. Descarca si instaleaza Git si Python 3.
2. Creeaza pe GitHub doua depozite PUBLICE:
   - exercitiu-git (bifeaza Add a README file)
   - exercitiu-2 (NU bifa Add a README file)
3. Inlocuieste USERNAME din comenzile de mai jos cu numele tau GitHub.
4. Autentificarea GitHub se face in browser la primul git push.

CONTINUT:
- exercitiu-git/: fisierele pentru Lucrarea A si B.
- exercitiu-2/: README pentru al doilea depozit.
- depanare/: programul functional inventar.py, datele de test si raportul generat.

LUCRAREA A - exercitiu-git
Daca ai creat deja depozitul gol pe GitHub cu README:
  cd $HOME
  git clone https://github.com/USERNAME/exercitiu-git.git
  Copy-Item -Recurse -Force ".\laboratorul7\exercitiu-git\*" ".\exercitiu-git\"
  cd .\exercitiu-git
  git config --global user.name "Numele Prenumele"
  git config --global user.email "EMAILUL_CONTULUI_GITHUB"
  git config --global init.defaultBranch main
  git config --global pull.rebase false
  git add README.md salut.py .gitignore
  git commit -m "Adaug fisierele initiale"
  git push

NOTA: Daca README.md exista deja si nu ai modificat nimic, Git poate include
doar fisierele noi. Este normal.

Pentru a demonstra comenzile cerute:
  python salut.py
  git status
  git log --oneline
  git diff

Modifica salut.py, apoi ruleaza git diff. Pentru a anula modificarea:
  git restore salut.py

Pentru .gitignore:
  python -m venv .venv
  git status --short
  git add .gitignore
  git commit -m "Ignor mediul virtual"
  git push

Pentru testarea git pull:
- Deschide README.md pe GitHub, apasa Edit, adauga un rand si salveaza
  prin Commit changes.
- In terminal, in depozitul exercitiu-git:
  git pull
  type README.md

LUCRAREA A - exercitiu-2
Copiaza folderul laboratorul7\exercitiu-2 in folderul tau de lucru, apoi:
  cd $HOME
  Copy-Item -Recurse ".\laboratorul7\exercitiu-2" ".\exercitiu-2"
  cd .\exercitiu-2
  git init
  git add README.md
  git commit -m "Primul commit"
  git remote add origin https://github.com/USERNAME/exercitiu-2.git
  git branch -M main
  git push -u origin main

LUCRAREA B - depanare
In depozitul exercitiu-git, copiaza folderul depanare din acest pachet.
Daca l-ai copiat deja impreuna cu toate fisierele de la inceput, ruleaza:
  cd $HOME\exercitiu-git\depanare
  python inventar.py tinte.json --prag 1000
  python inventar.py tinte.json

Rezultatul pentru --prag 1000 trebuie sa fie:
Tinte citite: 6
sar peste 192.168.56.103 : port invalid abc
ssh: [22]
http: [80, 8080]
mysql: [3306]
necunoscut: [5432]
Peste 1000: ['192.168.56.102', '192.168.56.103', '192.168.56.104']
Raport salvat in raport_inventar.json

Apoi, din folderul exercitiu-git:
  git add depanare
  git commit -m "Adaug unealta inventar reparata si raportul"
  git push

LIMITARE IMPORTANTA PENTRU LUCRAREA B:
Fisa profesorului cere 10 reparatii separate, fiecare cu propriul commit,
pornind de la inventar.py intentionat defect, descarcat de pe ELSE.
Fisierul original defect nu a fost atasat in conversatie. De aceea, acest
pachet contine varianta finala functionala si date de test compatibile cu
iesirea ceruta, dar NU inventeaza cele 10 defecte si NU pretinde ca exista
10 commit-uri autentice de reparare. Pentru a realiza exact B2-B5, este
necesar fisierul original inventar.py si tinte.json de pe ELSE.

La final verifica:
  git log --oneline
  git status
  git push

Nu publica parole sau tokenuri GitHub in fisiere.
