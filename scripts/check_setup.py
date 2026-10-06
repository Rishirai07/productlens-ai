"""Checks that Stage 1 setup worked. Run: python scripts/check_setup.py"""
import importlib
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ok = True


def check(label, passed, hint=""):
    global ok
    print(f"  [{'OK' if passed else 'X '}] {label}" + ("" if passed else f"  -> {hint}"))
    ok = ok and passed


print("\nProductLens AI setup check\n")

v = sys.version_info
check(f"Python {v.major}.{v.minor}", v >= (3, 11), "Install Python 3.11 or newer")
check("Running inside .venv", sys.prefix != sys.base_prefix,
      "Activate it: .venv\\Scripts\\activate (Windows) or source .venv/bin/activate")

for pkg, mod in [("chromadb", "chromadb"), ("streamlit", "streamlit"), ("pandas", "pandas"),
                 ("python-dotenv", "dotenv"), ("pypdf", "pypdf"),
                 ("google-play-scraper", "google_play_scraper")]:
    try:
        importlib.import_module(mod)
        check(f"Package {pkg}", True)
    except ImportError:
        check(f"Package {pkg}", False, "pip install -r requirements.txt")

for folder in ["data/raw", "data/processed", "src", "evals", "tests", "scripts"]:
    check(f"Folder {folder}/", (ROOT / folder).is_dir(), f"Create the {folder} folder")

check(".env file exists", (ROOT / ".env").exists(), "Copy .env.example to .env")
gi = (ROOT / ".gitignore").read_text() if (ROOT / ".gitignore").exists() else ""
check(".env is ignored by Git", ".env" in gi.split(), "Add .env to .gitignore")

# The provider key is only needed from Stage 3 onward, so this is a warning, not a failure.
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
    provider = os.getenv("LLM_PROVIDER", "").lower()
    key = os.getenv(f"{provider.upper()}_API_KEY", "") if provider else ""
    print(f"  [{'OK' if key else '--'}] API key for '{provider or 'none'}'"
          + ("" if key else "  (not needed until Stage 3)"))
except ImportError:
    pass

print("\nAll good, Stage 1 is complete!\n" if ok else "\nFix the items marked X, then run this again.\n")
sys.exit(0 if ok else 1)
