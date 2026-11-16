"""Verificare locala pentru Laboratorul 8 (A + B). Rulare: python VERIFICARE_AUTOMATA.py"""
from pathlib import Path
import subprocess
import sys
import json

ROOT = Path(__file__).resolve().parent
GIT = ROOT / 'exercitiu-git'
GIT2 = ROOT / 'exercitiu-2'
DEP = GIT / 'depanare'
EXPECTED = """Tinte citite: 6
sar peste 192.168.56.103 : port invalid abc
ssh: [22]
http: [80, 8080]
mysql: [3306]
necunoscut: [5432]
Peste 1000: ['192.168.56.102', '192.168.56.103', '192.168.56.104']
Raport salvat in raport_inventar.json"""

def command(args, cwd):
    p = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if p.returncode:
        raise AssertionError(f"Comanda {args} a esuat:\n{p.stderr}")
    return p.stdout.strip()

def check(name, fn):
    try:
        fn()
        print(f'[OK] {name}')
        return True
    except Exception as exc:
        print(f'[EROARE] {name}: {exc}')
        return False

def eq(actual, expected):
    assert actual == expected, f'Asteptat {expected!r}, obtinut {actual!r}'

def test_git():
    log = command(['git','log','--format=%s'], GIT).splitlines()
    assert len(log) >= 17, f'Prea putine commituri: {len(log)}'
    assert 'Pornire: inventar.py stricat' in log
    assert 'Raportul uneltei reparate' in log
    assert len(log[1:11]) == 10
    assert (GIT/'.git').is_dir() and (GIT2/'.git').is_dir()

def test_b():
    eq(command([sys.executable,'inventar.py','tinte.json','--prag','1000'], DEP), EXPECTED)
    data=json.loads((DEP/'raport_inventar.json').read_text(encoding='utf-8'))
    eq(data['prag'],1000)
    eq(data['total_tinte'],6)
    eq(data['servicii'], {'ssh':[22], 'http':[80,8080], 'mysql':[3306], 'necunoscut':[5432]})
    eq(data['peste_prag'], ['192.168.56.102','192.168.56.103','192.168.56.104'])

results = [
    check('Lucrarea A: salut.py', lambda: eq(command([sys.executable,'salut.py'], GIT), 'Salut, GitHub!')),
    check('Lucrarea A: exemplu.py', lambda: eq(command([sys.executable,'exemplu.py'], GIT2), 'Al doilea depozit Git functioneaza!')),
    check('Lucrarea A+B: istoricul Git local', test_git),
    check('Lucrarea B: iesirea si raportul pentru prag 1000', test_b),
]
print('\nRezultat:', sum(results), '/', len(results), 'verificari locale reusite')
print('Operatiile online GitHub nu sunt testate de acest script.')
sys.exit(0 if all(results) else 1)
