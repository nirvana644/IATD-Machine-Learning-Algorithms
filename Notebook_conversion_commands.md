# Conversion commands

These commands work on MacOs using the default shell (ZSH).

For GNU/Linux they should mostly work. But be aware that in most Linux distributions the default shell is Bash. Commands such as `setopt INTERACTIVE_COMMENTS` are ZSH-specific.

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

# This command might need to be run twice for the last image to be included in the PDF.
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 2 Lesson 2 — The Hitchhiker’s Guide to Feature Extraction" \
    week_2_feature_extraction.ipynb

python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 2 Lesson 2 — Preparing data for a machine learning model" \
    week_2_preparing_data.ipynb
    
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 2 Lesson 2 — Analysing the Mental Health Dataset questions" \
    week_2_preparing_data_helper.ipynb

python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 2 Lab 1 — Matildas Exploratory Data Analysis (EDA)" \
    2_a_MatildasEDA.ipynb

# The command below will run the notebook. Therefore, any existing output will be recreated.
EXPORT_PDF=True python -m jupyter nbconvert \
    --execute \
    --ExecutePreprocessor.timeout=600 \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 2 Lab 2 — Sydney AirBnB Exploratory Data Analysis (EDA)" \
    2_b_SydneyAirbnbEDA.ipynb
    
# Run this notebook twice:
# 1. Set variable 'USE_STRATIFICATION=False' 
# 2. Run the notebook conversion TWICE
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --output="2_c_Airbnb_Splitting_Cleaning_Demo_no_stratify" \
    --LatexPreprocessor.title=$'Week 2 Lab 3 — Airbnb: clean, split, train, cross-validate, test\nNot Stratified' \
    2_c_Airbnb_Splitting_Cleaning_Demo.ipynb
# 1. Set variable 'USE_STRATIFICATION=True' and run the notebook. This must be the last value on the notebook as it's the default.
# 2. Run the notebook conversion TWICE
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --output="2_c_Airbnb_Splitting_Cleaning_Demo_stratify" \
    --LatexPreprocessor.title=$'Week 2 Lab 3 — Airbnb: clean, split, train, cross-validate, test\nStratified' \
    2_c_Airbnb_Splitting_Cleaning_Demo.ipynb
    
# Automated
setopt INTERACTIVE_COMMENTS
(
    # Stop immediately if execution or conversion fails.
    set -e

    notebook="2_c_Airbnb_Splitting_Cleaning_Demo.ipynb"

    for mode in False True; do
        if [[ "$mode" == "True" ]]; then
            suffix="stratify"
            subtitle="Stratified"
        else
            suffix="no_stratify"
            subtitle="Not Stratified"
        fi

        # Execute and save fresh outputs for this variant.
        USE_STRATIFICATION="$mode" python -m jupyter nbconvert \
            --to notebook \
            --execute \
            --inplace \
            --ExecutePreprocessor.timeout=600 \
            "$notebook"

        # Export the freshly saved outputs to PDF.
        python -m jupyter nbconvert \
            --to pdf \
            --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
            --template=templates \
            --output-dir="./notebook_pdf" \
            --output="2_c_Airbnb_Splitting_Cleaning_Demo_${suffix}" \
            --LatexPreprocessor.title=$'Week 2 Lab 3 — Airbnb: clean, split, train, cross-validate, test\n'"$subtitle" \
            "$notebook"
    done
)
```

## Week 3: Building classification models with supervised learning

```bash
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 3 Lesson 2 — Sigmoid function" \
    week_3_lesson_2_sigmoid_func.ipynb

# This needs to be run twice so that the image on the last page is included in the PDF    
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 3 Lesson 2 — Question 2 Naive Bayes" \
    week_3_lesson_2_question_2.ipynb
    
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 3 Lesson 2 — Question 3 Naive Bayes" \
    week_3_lesson_2_question_3.ipynb
    
# Decision tree. There are 4 decision tree notebooks.
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 3 Lesson 2 — Decision Tree Algorithm, Explained" \
    week_3_decision_tree_1.ipynb
    
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 3 Lesson 2 — Decision tree - Classification" \
    week_3_decision_tree_2_classification.ipynb

# This needs to be run twice so that the last plotted graph is included in the final PDF.       
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 3 Lesson 2 — Decision Tree Regression" \
    week_3_decision_tree_3_regression.ipynb

python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 3 Lesson 2 — Decision Tree \& Random Forest" \
    week_3_decision_tree_4_random-forest-for-beginners.ipynb
    
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 3 Lesson 2 — IBM HR Analytics Employee Attrition & Performance\nDataset exploration" \
    week_3_decision_tree_4_dataset_exploration.ipynb
    
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 3 Lesson 2 — Naive Bayes applied to Restaurant Reviews" \
    week_3_naive_bayes_reviews.ipynb

# This will delete existing outputs. You might need to run it twice.
EXPORT_PDF=True python -m jupyter nbconvert \
    --execute \
    --ExecutePreprocessor.timeout=600 \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 3 Lab 1 — Logistic Regression Breast Cancer" \
    3_a_LogisticRegression_BreastCancer.ipynb
    
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 3 Lab 2 — Predicting Heart Disease with Naive Bayes" \
    3_b_NaiveBayes_FraminghamCHD.ipynb
    
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title=$'Week 3 Lab 2 — Predicting Heart Disease with Naive Bayes\nImproved version with respect to the original class one' \
    3_b_NaiveBayes_Improved.ipynb
```

## Week 4: Discovering patterns with K-Means Clustering

```bash
python -m jupyter nbconvert \
    --to pdf \
    --TemplateExporter.extra_template_basedirs="./notebook_pdf" \
    --template=templates \
    --output-dir="./notebook_pdf" \
    --LatexPreprocessor.title="Week 4 Lesson 2 — K-Nearest Neighbors" \
    week_4_lesson_2_k_neighbours.ipynb
```

## Week 5: Learning from limited labels and hidden patterns

## Week 6: Optimising and enhancing machine learning models

## Extra

### Tables spanning multiple PDF pages

In `week_3_decision_tree_3_regression.ipynb`, `display_table(summary)` now
generates a LaTeX `longtable`, allowing page breaks and repeated column headers.
You can also request this explicitly with `display_table(summary, multipage=True)`.

Rerun the cell defining `display_table`, then rerun the table-display cells and
save the notebook before running the existing PDF export command. Without
`--execute`, nbconvert exports saved outputs, including any old single-page tables.

`fit_to_page=True` uses a single-page resizing box and disables automatic
multipage output. Do not combine it with `multipage=True`; resizing boxes cannot
break across pages. For a long table, leave `fit_to_page=False` (the default).
Use `multipage=False` to explicitly retain a normal single-page table.

```bash
# Finding notebooks bigger than 1MB
# This is useful to avoid uploading super large noteabook to GitHub
find . -maxdepth 1 -type f -name '*.ipynb' -size +1048576c -exec ls -lh {} +
```
