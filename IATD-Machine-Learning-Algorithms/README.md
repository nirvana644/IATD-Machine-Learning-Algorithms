# IATD Machine Learning Algorithms

Lab notebooks, datasets and environment definition for the IATD
*Machine Learning Algorithms* microskill. A machine built from this
repository reproduces the exact environment every lab has been
verified against.

## Structure

| Week | Notebooks | Data |
|---|---|---|
| 1 | `1_a` Numpy refresher · `1_b` Pandas refresher · `1_c` Matplotlib refresher | `data/matildas.csv` |
| 2 | `2_a` Matildas EDA · `2_b` Sydney Airbnb EDA | `data/matildas.csv` · `data/sydney_airbnb.csv` |
| 3 | `3_a` Logistic Regression · `3_b` Naive Bayes | `data/breast-cancer.csv` · `data/framingham.csv` |
| 4 | `4_a` / `4_b` K-Means clustering | `data/countries.csv` · `data/studentseffort.csv` |
| 5 | `5_a` Apriori · `5_b` Label Spreading · `5_c` Label Propagation | `data/bread_basket.csv` (5_b/5_c use scikit-learn's iris) |
| 6 | `6_a` K-Means + PCA · `6_b` LDA · `6_c` PCA + Grid Search | `data/Wine.csv` (6_c uses scikit-learn's wine) |
| 7 | assessment dataset only — see `assignment/` | `assignment/segmented_customers_assessment_dataset.csv` |

Lab instructions are written into the notebooks themselves — each one
is a self-guided, step-by-step document. **No assessment solutions are
stored in this repository.**

## Getting started

**On the pre-built VM:** open the repo folder in VS Code, pick the
`iatd` Python environment as the kernel, open a notebook and run the
first cell.

**Building a machine (Windows):** run `provision/provision_windows.ps1`
in an elevated PowerShell. It installs Miniconda, creates the `iatd`
environment with Python 3.12.7 and the pinned packages, installs
VS Code with the Python and Jupyter extensions, and finishes by
running the smoke test.

**VS Code devcontainer / Codespaces:** open the repo in a container —
`.devcontainer/devcontainer.json` builds the same environment
automatically.

## Environment (pinned deliberately)

Python **3.12.7** · numpy **1.26.4** · pandas **2.2.2** · scipy
**1.13.1** · scikit-learn **1.5.1** · matplotlib **3.9.2** · seaborn
**0.13.2** · joblib **1.4.2** · plotly **5.24.1** · mlxtend **0.23.4**

The pins are not habit — newer releases change behaviour these lessons
depend on (scikit-learn altered K-Means defaults after 1.4; newer
mlxtend forces incompatible numpy/pandas upgrades; pandas 3 removes
methods the labs teach). Do not upgrade without re-running
`provision/smoke_test.py`, which executes every notebook headless and
verifies the versions.

## Data sources

- **matildas.csv** — every Australia women's international from
  January 2015, compiled from the public match record (Wikipedia
  results pages, cross-checked against the open results dataset by
  Mart Jürisoo). `matildas_source.csv` carries per-match dates and
  attendance sourcing. Penalty-shootout matches are recorded as draws.
- **sydney_airbnb.csv** — Inside Airbnb (insideairbnb.com), Sydney
  snapshot 16 June 2026, used under **CC BY 4.0**; curated to 34
  columns with prices parsed to numbers.
- **breast-cancer.csv / framingham.csv / countries.csv /
  studentseffort.csv / bread_basket.csv / Wine.csv** — teaching
  datasets carried over from the existing course materials.

© TAFE NSW — course materials for the IATD Machine Learning Algorithms
microskill. Datasets remain under their own licences as noted above.
