from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def main():
    etape = [(ROOT, ["-m", "arsenal.forensics.amprente", "arsenal/forensics/probe"]), (ROOT, ["-m", "pytest", "-q", "arsenal/forensics/test_amprente.py"]), (ROOT / "reparare", ["-m", "pytest", "-q"])]
    for cwd, args in etape:
        subprocess.run([sys.executable, *args], cwd=cwd, check=True)
    print("Toate verificarile au trecut.")

if __name__ == "__main__":
    main()
