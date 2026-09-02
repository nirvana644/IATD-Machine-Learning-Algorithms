"""IATD Machine Learning Algorithms - build verification.

Executes every lab notebook top-to-bottom in a headless kernel and
checks the pinned package versions. A clean pass means the machine
reproduces the environment the labs were verified against.

Usage:  python provision/smoke_test.py          (from the repo root or provision/)
Exit:   0 = all labs pass, 1 = something failed.
"""
import glob
import os
import sys
import time

EXPECTED = {
    "numpy": "1.26.4",
    "pandas": "2.2.2",
    "scipy": "1.13.1",
    "sklearn": "1.5.1",
    "matplotlib": "3.9.2",
    "seaborn": "0.13.2",
    "joblib": "1.4.2",
    "plotly": "5.24.1",
    "mlxtend": "0.23.4",
}

def check_versions():
    import importlib
    bad = []
    for mod, want in EXPECTED.items():
        try:
            have = importlib.import_module(mod).__version__
        except ModuleNotFoundError:
            have = "MISSING"
        mark = "OK " if have == want else "BAD"
        print(f"  [{mark}] {mod:12s} want {want:10s} have {have}")
        if have != want:
            bad.append(mod)
    return bad

def run_notebooks():
    import nbformat
    from nbclient import NotebookClient
    failures = []
    for nb_path in sorted(glob.glob("*.ipynb")):
        t0 = time.time()
        try:
            nb = nbformat.read(nb_path, as_version=4)
            NotebookClient(nb, timeout=900, kernel_name="python3").execute()
            print(f"  [OK ] {nb_path}  ({time.time()-t0:.0f}s)")
        except Exception as exc:
            print(f"  [BAD] {nb_path}  ({time.time()-t0:.0f}s)  {type(exc).__name__}")
            failures.append(nb_path)
    return failures

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    print("Package versions:")
    bad_versions = check_versions()
    try:
        import nbclient  # noqa: F401
    except ModuleNotFoundError:
        os.system(f"{sys.executable} -m pip install -q nbclient nbformat")
    print("\nExecuting notebooks (the grid-search lab takes a few minutes):")
    failed = run_notebooks()
    print()
    if bad_versions or failed:
        print(f"SMOKE TEST FAILED - version mismatches: {bad_versions or 'none'}; "
              f"notebook failures: {failed or 'none'}")
        sys.exit(1)
    print("SMOKE TEST PASSED - environment matches and all labs run clean.")
