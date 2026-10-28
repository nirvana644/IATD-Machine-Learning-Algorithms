# Jupyter Notebook Recovery Guide

This guide explains what to do if a Jupyter notebook (`.ipynb`) becomes too large, appears corrupted, freezes PyCharm/Jupyter, or fails to open after a bad save/export/overwrite.

## Symptoms

You may see one or more of these:

- PyCharm says the notebook is corrupted.
- Jupyter/PyCharm hangs when opening the notebook.
- The notebook file is hundreds of MBs or several GBs.
- The notebook is valid JSON but still will not open.
- A cell with huge output was accidentally saved.
- Removing the last cell did not reduce the file size.
- The notebook opens in a text editor but not in PyCharm/Jupyter.

## First Rule: Make a Backup

Before attempting any repair, copy the notebook.

```bash
cp week_2_feature_extraction.ipynb week_2_feature_extraction.backup.ipynb
```

For a different notebook, replace the filename:

```bash
cp your_notebook.ipynb your_notebook.backup.ipynb
```

Do not continue until you have a backup.

## 1. Check Whether the Notebook Is Valid JSON

A Jupyter notebook is a JSON file. It should usually start like this:

```json
{
 "cells": [
  {
```

Check the first few lines:

```bash
head -n 5 week_2_feature_extraction.ipynb
```

Validate the JSON:

```bash
python -m json.tool week_2_feature_extraction.ipynb > /tmp/notebook_check.json
echo $?
```

If the result is:

```text
0
```

then the file is valid JSON.

If you get an error, the notebook file is malformed JSON and should be recovered from a backup, Git, PyCharm Local History, or a Jupyter checkpoint.

## 2. Check the File Size

Large notebooks often fail to open because they contain huge saved outputs.

```bash
ls -lah week_2_feature_extraction.ipynb
```

A normal notebook might be KBs or a few MBs.

A very large notebook, for example hundreds of MBs, usually means one or more cells contain massive output.

## 3. Check Whether `nbformat` Can Read the Notebook

Run:

```bash
python - <<'PY'
import nbformat

path = "week_2_feature_extraction.ipynb"

with open(path, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

print("Notebook is readable by nbformat")
print("Cells:", len(nb.cells))
print("nbformat:", nb.nbformat, nb.nbformat_minor)
PY
```

If this works, the notebook structure is probably valid.

If this fails, copy the full error message and recover from backup, Git, Local History, or checkpoints.

## 4. Identify the Largest Cells

Use this script to find which cells are making the notebook huge:

```bash
python - <<'PY'
import json

path = "week_2_feature_extraction.ipynb"

with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

sizes = []

for i, cell in enumerate(nb.get("cells", [])):
    size = len(json.dumps(cell))
    source = "".join(cell.get("source", ""))
    preview = source[:120].replace("\n", "\\n")
    sizes.append((size, i, cell.get("cell_type"), preview))

for size, i, typ, preview in sorted(sizes, reverse=True)[:20]:
    print(f"Cell {i}: {size / 1024 / 1024:.2f} MB | {typ} | {preview}")
PY
```

This prints the largest cells in descending order.

If one cell is hundreds of MBs, that cell probably contains massive output.

## 5. Remove Only the Last Cell

If the bad cell is the last cell, remove it safely:

```bash
python - <<'PY'
import nbformat
from pathlib import Path

path = Path("week_2_feature_extraction.ipynb")

with path.open("r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

print("Original cell count:", len(nb.cells))

if nb.cells:
    last = nb.cells[-1]
    print("Removing last cell")
    print("Last cell type:", last.get("cell_type"))
    print("Last cell source preview:")
    print("".join(last.get("source", ""))[:500])
    nb.cells.pop()

print("New cell count:", len(nb.cells))

with path.open("w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print("Saved notebook after removing last cell.")
PY
```

Then check the size:

```bash
ls -lah week_2_feature_extraction.ipynb
```

If the size drops significantly, the problem was likely the last cell.

## 6. Clear All Outputs

If the notebook is still huge, the issue is probably saved outputs in earlier cells.

This removes all code cell outputs but keeps code and Markdown.

```bash
python - <<'PY'
import nbformat
from pathlib import Path

path = Path("week_2_feature_extraction.ipynb")

with path.open("r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

removed_outputs = 0

for cell in nb.cells:
    if cell.get("cell_type") == "code":
        removed_outputs += len(cell.get("outputs", []))
        cell["outputs"] = []
        cell["execution_count"] = None

with path.open("w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print(f"Cleared {removed_outputs} outputs.")
print(f"Cell count: {len(nb.cells)}")
PY
```

Then check the size again:

```bash
ls -lah week_2_feature_extraction.ipynb
```

This is often the most effective fix.

## 7. Clear Outputs Using `jupyter nbconvert`

If Jupyter is installed, this is a simple alternative:

```bash
jupyter nbconvert --clear-output --inplace week_2_feature_extraction.ipynb
```

Then verify:

```bash
ls -lah week_2_feature_extraction.ipynb
```

## 8. Remove a Specific Cell by Index

If the largest-cell script says the bad cell is, for example, cell `17`, remove only that cell:

```bash
python - <<'PY'
import nbformat
from pathlib import Path

path = Path("week_2_feature_extraction.ipynb")
cell_index_to_remove = 17

with path.open("r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

print("Original cell count:", len(nb.cells))

if 0 <= cell_index_to_remove < len(nb.cells):
    cell = nb.cells[cell_index_to_remove]
    print(f"Removing cell {cell_index_to_remove}")
    print("Cell type:", cell.get("cell_type"))
    print("Cell source preview:")
    print("".join(cell.get("source", ""))[:500])
    del nb.cells[cell_index_to_remove]
else:
    raise IndexError("Cell index out of range")

print("New cell count:", len(nb.cells))

with path.open("w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print("Saved notebook after removing selected cell.")
PY
```

Change this line as needed:

```python
cell_index_to_remove = 17
```

## 9. Save a Repaired Copy Instead of Overwriting

If you do not want to overwrite the original notebook immediately, write to a new file:

```bash
python - <<'PY'
import nbformat
from pathlib import Path

source = Path("week_2_feature_extraction.ipynb")
target = Path("week_2_feature_extraction_fixed.ipynb")

with source.open("r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

for cell in nb.cells:
    if cell.get("cell_type") == "code":
        cell["outputs"] = []
        cell["execution_count"] = None

with target.open("w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print(f"Saved repaired notebook to {target}")
PY
```

Open the fixed file first. If it looks good, replace the original:

```bash
mv week_2_feature_extraction_fixed.ipynb week_2_feature_extraction.ipynb
```

## 10. Recover from Git

If the file is tracked by Git, check its status:

```bash
git status
```

See whether the notebook has changed:

```bash
git diff -- week_2_feature_extraction.ipynb
```

Restore the notebook from the last commit:

```bash
git checkout -- week_2_feature_extraction.ipynb
```

Or, with newer Git syntax:

```bash
git restore week_2_feature_extraction.ipynb
```

Warning: this discards uncommitted changes to that file.

## 11. Recover from PyCharm Local History

If Git cannot help, PyCharm Local History may still have a good copy.

Steps:

1. Right-click the notebook in the PyCharm Project pane.
2. Select **Local History**.
3. Select **Show History**.
4. Find a version before the corruption.
5. Revert it or copy the contents into a new file.

This is often the best recovery option if the notebook was not committed to Git.

## 12. Recover from Jupyter Checkpoints

Search for checkpoint files:

```bash
find . -path "*ipynb_checkpoints*" -type f
```

You may find something like:

```text
./.ipynb_checkpoints/week_2_feature_extraction-checkpoint.ipynb
```

Copy it back:

```bash
cp ./.ipynb_checkpoints/week_2_feature_extraction-checkpoint.ipynb week_2_feature_extraction.ipynb
```

Then validate it:

```bash
python -m json.tool week_2_feature_extraction.ipynb > /tmp/notebook_check.json
echo $?
```

## 13. Important Filename Notes

Do not put backticks around filenames in shell commands.

Correct:

```bash
mv fixed_notebook.ipynb week_2_feature_extraction.ipynb
```

Also correct and safer if filenames contain spaces:

```bash
mv "fixed_notebook.ipynb" "week_2_feature_extraction.ipynb"
```

Avoid:

```bash
mv fixed_notebook.ipynb `week_2_feature_extraction.ipynb`
```

Backticks in the shell mean command substitution.

## 14. Prevention Tips

Clear outputs before committing notebooks:

```bash
jupyter nbconvert --clear-output --inplace week_2_feature_extraction.ipynb
```

Check notebook size regularly:

```bash
ls -lah *.ipynb
```

Commit working notebooks to Git:

```bash
git add week_2_feature_extraction.ipynb
git commit -m "Save working feature extraction notebook"
```

Save repaired versions under a new name first, for example:

```text
week_2_feature_extraction_fixed.ipynb
```

Open the fixed file and confirm it works before replacing the original.

## Quick Emergency Command Sequence

Use this when a notebook is huge but valid JSON:

```bash
cp week_2_feature_extraction.ipynb week_2_feature_extraction.backup.ipynb

python -m json.tool week_2_feature_extraction.ipynb > /tmp/notebook_check.json
echo $?

ls -lah week_2_feature_extraction.ipynb

python - <<'PY'
import nbformat
from pathlib import Path

path = Path("week_2_feature_extraction.ipynb")

with path.open("r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

for cell in nb.cells:
    if cell.get("cell_type") == "code":
        cell["outputs"] = []
        cell["execution_count"] = None

with path.open("w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print("Cleared all outputs.")
print("Cells:", len(nb.cells))
PY

ls -lah week_2_feature_extraction.ipynb
```

Then reopen the notebook in PyCharm or Jupyter.

## Final Checklist

After repair, validate the JSON:

```bash
python -m json.tool week_2_feature_extraction.ipynb > /tmp/notebook_check.json
echo $?
```

Expected:

```text
0
```

Then validate with `nbformat`:

```bash
python - <<'PY'
import nbformat

path = "week_2_feature_extraction.ipynb"

with open(path, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

print("Notebook OK")
print("Cells:", len(nb.cells))
PY
```

If both commands work, the notebook is structurally valid.