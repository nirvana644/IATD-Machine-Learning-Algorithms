# Conversion commands


## General

Create the notebooks output folder:

```bash
mkdir -p ./notebook_pdf
```


## Week 1

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
```

## Week 2

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
```