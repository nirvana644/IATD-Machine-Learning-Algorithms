# Conversion commands


## General

Create the notebooks output folder:

```bash
mkdir -p ./notebook_pdf
```


## Week 1: Python data science foundations refresher

```bash
# Simple version
python -m jupyter nbconvert --to pdf \
    --output-dir="./notebook_pdf" \
    week_1_lesson_3.ipynb
    
# With styles
# Not required: TEXINPUTS="$PWD/notebook_pdf/templates:${TEXINPUTS:-}:"
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 1 Lesson 3" \
    week_1_lesson_3.ipynb
    
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 1 Lesson 4 — Duplicates, Outliers, Missing Data and Checking Data" \
    week_1_lesson_4_duplicates.ipynb
    
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 1 Lesson 4 — Preprocessing data with Scikit" \
    week_1_lesson_4_scikit.ipynb
    
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 1 Lab 1 — Numpy Refresher" \
    1_a_NumpyRefresher.ipynb

python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 1 Lab 2 — Pandas Dataframe Refresher" \
    1_b_PandasRefresher.ipynb

python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 1 Lab 3 — Matplotlib Refresher" \
    1_c_MatplotlibRefresher.ipynb
```

You can make a notebook landscape. However, in the case of dataframes, it seems pandas already splits the row, so it is to no avail.

```bash
# This is a special case where we want to use a different template for the notebook, so we specify the template path and name explicitly.
# It will be on landscape orientation, so that a wide table row can fit in the page.
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --TemplateExporter.extra_template_paths="./notebook_pdf" \
    --template=landscape \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 1 Lab 2 — Pandas Dataframe Refresher" \
    1_b_PandasRefresher.ipynb
```

## Week 2: Exploring and understanding data with EDA

```bash
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 2 Lesson 2 — Mean Square Error (MSE)" \
    week_2_lesson_2_mse.ipynb
    
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 2 Lesson 2 — Regularisation using L1 (Lasso) and L2 (Ridge)" \
    week_2_lesson_2_regularisation.ipynb

python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 2 Lesson 2 — The Hitchhiker’s Guide to Feature Extraction
" \
    week_2_feature_extraction.ipynb

python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 2 Lab 1 — Matildas Exploratory Data Analysis (EDA)" \
    2_a_MatildasEDA.ipynb

python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 2 Lab 2 — Sydney AirBnB Exploratory Data Analysis (EDA)" \
    2_b_SydneyAirbnbEDA.ipynb
```

## Week 3: Building classification models with supervised learning

## Week 4: Discovering  patterns with K-Means Clustering

## Week 5: Learning from limited labels and hidden patterns

## Week 6: Optimising and enhancing machine learning models
