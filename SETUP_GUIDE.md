# Setup Guide for Lab Mates

Two main scenarios: **creating a new project** or **joining an existing project**.

## Scenario 1: Creating a New Project

### Prerequisites
- Mamba installed ([installation guide](https://mamba.readthedocs.io/en/latest/installation.html))
- Git ([installation guide](https://github.com/git-guides/install-git))
- VSCode ([installation guide](https://code.visualstudio.com/download), optional but recommended)

### Quick Start

```bash
# Get the setup script
bash setup-project.sh <project-name>
```

Open the project in VS Code. Open the terminal by navigating to `Terminal > New Terminal` and run the following commands

```bash
# Create mamba environment with uv as pip backend
mamba env create --use-uv -f environment.yml

# Set env name variable (this just automatically grabs the name of your project from environment.yml)
ENV_NAME=$(grep "^name:" environment.yml | awk '{print $2}')

# Activate it
mamba activate $ENV_NAME

# Install Jupyter kernel for this environment
python -m ipykernel install --user --name=$ENV_NAME --display-name "$ENV_NAME"
```

Then: Open `notebooks/example.ipynb` → select your kernel (same as your project name) → start coding!

## Scenario 2: Joining an Existing Project

Someone has already created the project and pushed it to GitHub.

### Step 1: Clone
```bash
git clone <repo-url>
cd <repo-name>
```

### Step 2: Create environment
```bash
mamba env create --use-uv -f environment.yml
```

This:
- Creates the environment with the exact Python version
- Installs all conda packages
- Uses uv to install pip packages (fast, reproducible)

### Step 3: Activate
```bash
# Set env name variable (this just automatically grabs the name of your project from environment.yml)
ENV_NAME=$(grep "^name:" environment.yml | awk '{print $2}')

# Activate it
mamba activate $ENV_NAME

# Install Jupyter kernel for this environment
python -m ipykernel install --user --name=$ENV_NAME --display-name "$ENV_NAME"
```

## Using Jupyter Notebooks in VSCode

### Opening a notebook
- Navigate to `notebooks/` folder
- Click any `.ipynb` file

### Selecting a kernel
- Top-right corner shows kernel selector
- Click it → choose your mamba environment
- If missing: reload VSCode (Cmd+Shift+P → "Developer: Reload Window")

### Running cells
- **Shift+Enter**: Run and move to next
- **Ctrl+Enter**: Run and stay
- Play button: Run current cell
- Ctrl+Shift+Alt+Enter: Run all cells

## Adding Packages

### If you need a new package:

1. **Edit `environment.yml`** — add to dependencies
   ```yaml
   dependencies:
     - python=3.11
     - numpy
     - requests  # Add here
   ```

2. **Update environment**
   ```bash
   mamba env update --use-uv -f environment.yml
   ```

3. **Commit**
   ```bash
   git add environment.yml
   git commit -m "Add requests dependency"
   ```

Lab mates then pull and run `mamba env update --use-uv -f environment.yml`.

## Key Files Explained

| File | Purpose |
|------|---------|
| `environment.yml` | Mamba environment: Python version, all dependencies |
| `pyproject.toml` | Project metadata, build config, tool settings |
| `notebooks/` | Your Jupyter notebooks |
| `src/` | Reusable Python modules |
| `data/` | Data files (excluded from git) |

## Recommended VSCode Extensions

Install when prompted, or manually:
- **Python** (ms-python.python)
- **Jupyter** (ms-toolsai.jupyter)
- **Pylance** (ms-python.vscode-pylance)
- **Black Formatter** (ms-python.black-formatter)
- **Ruff** (charliermarsh.ruff)

## Common Issues

### Kernel not showing
```bash
# Make sure environment is created
mamba env create --use-uv -f environment.yml

# Make sure it's activated in terminal
mamba activate <env-name>

# Reload VSCode
Cmd+Shift+P → "Developer: Reload Window"
```

### Import errors
```bash
# Recreate environment
mamba env remove -n <env-name>
mamba env create --use-uv -f environment.yml
mamba activate <env-name>
```

### Can't find mamba
- Install mamba: https://mamba.readthedocs.io/
- Or use conda (same commands, just slower)

## Development Workflow

Format code:
```bash
black .
```

Lint:
```bash
ruff check --fix .
```

Type check:
```bash
mypy src/
```

Run tests:
```bash
pytest
```

## Quick Commands Reference

```bash
# Environment
mamba env create --use-uv -f environment.yml
mamba env update --use-uv -f environment.yml
mamba activate <env-name>
mamba deactivate
mamba env list

# Git
git status
git add .
git commit -m "message"
git push
git pull
```

## Resources

- **Mamba**: https://mamba.readthedocs.io/
- **UV**: https://docs.astral.sh/uv/
- **Jupyter**: https://jupyter.org/
- **VSCode Jupyter**: https://code.visualstudio.com/docs/datascience/jupyter-notebooks
