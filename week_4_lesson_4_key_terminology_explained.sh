#!/usr/bin/env bash
set -Eeuo pipefail

# chmod +x week_4_lesson_4_key_terminology_explained.sh
# ./week_4_lesson_4_key_terminology_explained.sh

# Stop and report the command and line if an error occurs.
trap 'echo "Error on line $LINENO: $BASH_COMMAND" >&2' ERR

NOTEBOOK="week_4_lesson_4_key_terminology_explained.ipynb"
OUTPUT_DIR="./notebook_pdf"
TEX_NAME="week4_pdf_build_pca"
PDF_NAME="week_4_lesson_4_key_terminology_explained"

# Step 1: Export notebook to LaTeX.
# This also converts embedded images, including SVGs, as needed.
echo "Step 1: Exporting notebook to LaTeX..."

python -m jupyter nbconvert \
    --to latex \
    --TemplateExporter.extra_template_basedirs="$OUTPUT_DIR" \
    --template=templates \
    --output-dir="$OUTPUT_DIR" \
    --output="$TEX_NAME" \
    --LatexPreprocessor.title="Week 4 Lesson 5 — Variance, Covariance, Eigenvalues and Eigenvectors" \
    --LatexPreprocessor.author_names="Álvaro Morán Gago" \
    "$NOTEBOOK"


# Step 2: Replace MathJax syntax with XeLaTeX-compatible syntax
# \centernot\implies -> \nLongrightarrow
python - <<'PY'
from pathlib import Path

path = Path("./notebook_pdf/week4_pdf_build_pca.tex")
text = path.read_text(encoding="utf-8")

old = r"\centernot\implies"
new = r"\not\Longrightarrow"

count = text.count(old)
text = text.replace(old, new)

path.write_text(text, encoding="utf-8")

print(f"Replaced {count} occurrence(s) of {old} with {new}")
PY

# Step 2: Replace the problematic heading with a labelled subsection.
echo "Step 2: Fixing LaTeX subsection..."

TEX_PATH="$OUTPUT_DIR/$TEX_NAME.tex" python - <<'PY'
import os
from pathlib import Path

path = Path(os.environ["TEX_PATH"])
text = path.read_text(encoding="utf-8")

old = r"\#\# 6. From covariance to PCA"
new = r"\subsection{6. From covariance to PCA}\label{section-6}"

if old not in text:
    raise SystemExit("Expected heading not found; no changes made.")

text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print("Created subsection with label section-6.")
PY

# Step 3: Compile LaTeX to PDF twice.
# The second pass resolves cross-references, labels and page numbers.
for pass in 1 2; do
    echo "Step 3: Compiling PDF (pass $pass/2)..."

    TEXINPUTS="$OUTPUT_DIR//:" xelatex \
        -shell-escape \
        -interaction=nonstopmode \
        -halt-on-error \
        -output-directory="$OUTPUT_DIR" \
        -jobname="$PDF_NAME" \
        "$OUTPUT_DIR/$TEX_NAME.tex"
done


echo "PDF successfully generated: $OUTPUT_DIR/$PDF_NAME.pdf"
