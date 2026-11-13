#!/usr/bin/env bash
set -euo pipefail

PREFIX="week_4_lesson_3_"
NOTEBOOK="${PREFIX}apriori_vs_fp_growth.ipynb"
OUTPUT_DIR="./notebook_pdf"

DEFAULT_BASKETS='[
  ["bread", "milk"],
  ["bread", "diaper", "beer", "eggs"],
  ["milk", "diaper", "beer", "cola"],
  ["bread", "milk", "diaper", "beer"],
  ["bread", "milk", "diaper", "cola"]
]'

EGGS_BASKETS='[
  ["bread", "milk"],
  ["bread", "diaper", "beer", "eggs"],
  ["milk", "diaper", "beer", "cola"],
  ["bread", "milk", "diaper", "beer"],
  ["bread", "milk", "diaper", "cola"],
  ["eggs"]
]'

mkdir -p "$OUTPUT_DIR"

# Baseline: support 60%, confidence 75%, five baskets.
# Exercise 4: use the baseline PDF (00) to inspect milk's node counts.
# No additional export needed.
env \
  BASKETS_JSON="$DEFAULT_BASKETS" \
  MIN_SUPPORT=0.60 \
  MIN_CONFIDENCE=0.75 \
  BASKET_MULTIPLIER=200 \
  EXERCISE_TITLE="Baseline — original baskets" \
  python -m jupyter nbconvert \
    --execute --to webpdf \
    --ExecutePreprocessor.timeout=600 \
    --output="${PREFIX}00_baseline_support060_conf075_baskets05" \
    --output-dir="$OUTPUT_DIR" \
    "$NOTEBOOK"

# Exercise 1: lower support to 40%.
env \
  BASKETS_JSON="$DEFAULT_BASKETS" \
  MIN_SUPPORT=0.40 \
  MIN_CONFIDENCE=0.75 \
  BASKET_MULTIPLIER=200 \
  EXERCISE_TITLE="Exercise 1 — lower minimum support" \
  python -m jupyter nbconvert \
    --execute --to webpdf \
    --ExecutePreprocessor.timeout=600 \
    --output="${PREFIX}01_support040_conf075_baskets05" \
    --output-dir="$OUTPUT_DIR" \
    "$NOTEBOOK"

# Exercise 2: add an eggs-only basket; retain 60% support.
env \
  BASKETS_JSON="$EGGS_BASKETS" \
  MIN_SUPPORT=0.60 \
  MIN_CONFIDENCE=0.75 \
  BASKET_MULTIPLIER=200 \
  EXERCISE_TITLE="Exercise 2 — add an eggs-only basket" \
  python -m jupyter nbconvert \
    --execute --to webpdf \
    --ExecutePreprocessor.timeout=600 \
    --output="${PREFIX}02_added_eggs_support060_conf075_baskets06" \
    --output-dir="$OUTPUT_DIR" \
    "$NOTEBOOK"

# Exercise 3: raise confidence to 100%.
env \
  BASKETS_JSON="$DEFAULT_BASKETS" \
  MIN_SUPPORT=0.60 \
  MIN_CONFIDENCE=1.00 \
  BASKET_MULTIPLIER=200 \
  EXERCISE_TITLE="Exercise 3 — require 100% confidence" \
  python -m jupyter nbconvert \
    --execute --to webpdf \
    --ExecutePreprocessor.timeout=600 \
    --output="${PREFIX}03_support060_conf100_baskets05" \
    --output-dir="$OUTPUT_DIR" \
    "$NOTEBOOK"