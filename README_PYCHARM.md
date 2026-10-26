# Set Up the Machine Learning Environment

Use **Python 3.12** with the package versions supplied by the lab.

Note that Scikit-learn 1.4 and 1.5 supported Python 3.9—3.12 [official documentation](https://scikit-learn.org/stable/install.html#install-official-release).

The instructions below are for macOS. They may be slightly different for GNU/Linux.

## 1. Open the project folder

In Terminal, go to the project directory. Run a command similar to the one below:

```bash
cd ~/PycharmProjects/IATD-Machine-Learning-Algorithms
```

## 2. Check Python 3.12 is installed

```bash
python3.12 --version
```

The output should be `Python 3.12.x`. If the command is not found, install Python 3.12 before continuing.

## 3. Create the virtual environment

```bash
python3.12 -m venv .venv
```

This creates a `.venv` folder inside the project.

## 4. Activate the environment

On macOS:

```bash
source .venv/bin/activate
```

Verify the Python version and location:

```bash
python --version
which python
```

The version should be `3.12.x`, and the path should end in `.venv/bin/python`.

## 5. Create the requirements file

If there's no `requirements.txt` file, save the following content as `requirements.txt` in the project folder:

```text
# IATD Machine Learning Algorithms - pinned student environment
# These exact versions are what every lab is verified against.
# Do NOT upgrade without re-running provision/smoke_test.py:
# newer scikit-learn / pandas releases change behaviour the lessons rely on.
numpy==1.26.4
pandas==2.2.2
scipy==1.13.1
scikit-learn==1.5.1
matplotlib==3.9.2
seaborn==0.13.2
joblib==1.4.2
plotly==5.24.1
mlxtend==0.23.4

# Notebook tooling - pinned like everything else
ipykernel==6.29.5
nbformat==5.10.4
nbclient==0.10.0
```

## 6. Install and check the packages

With the environment activated, run:

```bash
python -m pip install -r requirements.txt
python -m pip check
```

The dependency check should report:

```text
No broken requirements found.
```

Note that if there's a notice message to update `pip`:

```bash
pip install --upgrade pip
```

Verify the main package versions:

```bash
python -c "import sklearn, numpy, pandas; print('scikit-learn:', sklearn.__version__); print('NumPy:', numpy.__version__); print('pandas:', pandas.__version__)"
```

Expected output:

```text
scikit-learn: 1.5.1
NumPy: 1.26.4
pandas: 2.2.2
```

If the lab includes its smoke test, run it from the project folder:

```bash
python provision/smoke_test.py
```

## 7. Configure PyCharm

1. Open the project in PyCharm.
2. Go to **PyCharm → Settings → Python → Interpreter**.
   In older versions, use **Project → Python Interpreter**.
3. Choose **Add Interpreter → Add Local Interpreter**.
4. Select **Existing environment**, under **Virtualenv** if applicable.
5. Select this interpreter (the one previously created) and verify the path is:

   ```text
   ~/PycharmProjects/IATD-Machine-Learning-Algorithms/.venv/bin/python
   ```

6. Click **OK / Apply** and ensure it is selected for the project.

PyCharm will use this environment when running the project.

For notebooks, also select this environment as the notebook kernel if prompted.

## 8. Use the environment in future terminal sessions

Activate it each time you open a new terminal:

```bash
cd ~/PycharmProjects/IATD-Machine-Learning-Algorithms
source .venv/bin/activate
```

To deactivate it:

```bash
deactivate
```

Terminal activation is separate from PyCharm's interpreter selection. PyCharm uses the configured interpreter directly.

## Keep the lab environment consistent

- Keep the package versions pinned in `requirements.txt`.
- Do not upgrade them without following the lab's verification instructions.
- If using Git, add `.venv/` to `.gitignore`.

The command below will add `.venv/` to `.gitignore` if it's not already there:
```bash
touch .gitignore
grep -Eq '^[[:space:]]*/?\.venv/?[[:space:]]*$' .gitignore ||
  printf '\n.venv/\n' >> .gitignore
```