# Install

1. Install conda (or equivalent e.g. miniconda, mamba, etc. and update following commands accordingly)
2. Create a new environment, with suitable python version and package manager package `poetry`:

```bash
conda create -n ping python=3.12 poetry
conda activate ping
```

3. Navigate to the directory where the `poetry.lock` file is located and run:

```bash
poetry install
```

If there are problems with installing `poetry`, when creating the environment, try instead:

```bash
conda create -n ping python=3.12
conda activate ping
pip install poetry
poetry install
```