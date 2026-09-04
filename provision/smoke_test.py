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

sys.stdout.reconfigure(line_buffering=True)

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

def check_infrastructure():
    """The packages the smoke test itself needs. All of them come from
    requirements.txt - if any is absent, the environment was never
    provisioned, and that is the finding (we do not quietly install
    things here: this is a verification tool, not an installer)."""
    missing = []
    for mod in ("nbformat", "nbclient", "ipykernel", "jupyter_client"):
        try:
            __import__(mod)
        except ModuleNotFoundError:
            missing.append(mod)
    return missing

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
            detail = " ".join(str(exc).split())
            if len(detail) > 300:
                detail = detail[:300] + " ..."
            print(f"  [BAD] {nb_path}  ({time.time()-t0:.0f}s)  {type(exc).__name__}: {detail}")
            failures.append(nb_path)
    return failures

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    print(f"Interpreter: {sys.executable}")
    print(f"Python:      {sys.version.split()[0]}")
    print("Package versions:")
    bad_versions = check_versions()

    infra_missing = check_infrastructure()
    if infra_missing:
        print()
        print(f"SMOKE TEST FAILED - this Python has no notebook tooling "
              f"(missing: {', '.join(infra_missing)}).")
        print("This means 'pip install -r requirements.txt' never ran against "
              "this interpreter. Provision the environment first:")
        print(f"  {sys.executable} -m pip install -r requirements.txt")
        print("(or re-run provision_windows.ps1 and watch for the step that fails)")
        sys.exit(1)

    print("\nExecuting notebooks (the grid-search lab takes a few minutes):")
    failed = run_notebooks()
    print()
    if bad_versions or failed:
        print(f"SMOKE TEST FAILED - version mismatches: {bad_versions or 'none'}; "
              f"notebook failures: {failed or 'none'}")
        sys.exit(1)
    print("SMOKE TEST PASSED - environment matches and all labs run clean.")
