# JupyterLab Setup Notes

## Context

- JupyterLab is launched via the `jlab` PowerShell function, which always starts from `C:\Users\droa\Documents\Workspace` using that directory's `.venv`.
- `claude-projects` is a **uv workspace** — all dependencies (pandas, plotly, etc.) are installed into `claude-projects/.venv`, not the parent Workspace venv.
- Because of this mismatch, notebooks see the wrong Python environment unless a dedicated kernel is registered.

---

## Fix 1 — Enable PowerShell Execution Policy

Required so that `profile.ps1` (which defines `jlab`, `uv-kernel-smart`, etc.) loads on startup.

Run **PowerShell as Administrator**:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Reboot or restart PowerShell after applying.

---

## Fix 2 — Register the claude-projects Kernel

From the `claude-projects` directory in PowerShell (after Fix 1 so profile is loaded):

```powershell
cd C:\Users\droa\Documents\Workspace\claude-projects
uv-kernel-smart
```

This uses your existing `uv-kernel-smart` profile function, which runs:

```powershell
uv run python -m ipykernel install --user --name claude-projects --display-name "Python (claude-projects)"
```

Alternatively, call it directly without the function:

```powershell
C:\Users\droa\Documents\Workspace\claude-projects\.venv\Scripts\python -m ipykernel install --user --name claude-projects --display-name "claude-projects"
```

---

## Fix 3 — Select the Correct Kernel in JupyterLab

1. Open JupyterLab via `jlab`
2. Open your notebook in `data-analysis/`
3. Click the kernel name (top-right) and switch to **"Python (claude-projects)"**

Verify it's correct inside the notebook:

```python
import sys
print(sys.executable)  # should point to claude-projects/.venv/Scripts/python.exe

import pandas as pd
print(pd.__version__)
```

---

## Useful Profile Functions (defined in profile.ps1)

| Function | What it does |
|---|---|
| `jlab` | Starts JupyterLab from `Workspace/` root |
| `uv-kernel-smart` | Registers current folder as a Jupyter kernel |
| `uv-kernel -Name X -DisplayName Y` | Registers kernel with explicit name |
| `uv-kernel-manage` | Lists kernels and lets you uninstall one |
| `jlist` | Lists all registered kernels |
| `jclean <name>` | Uninstalls a kernel by name |

---

## Why There Is No .venv in data-analysis/

`data-analysis` is a **uv workspace member** of `claude-projects`. All workspace members share the root `.venv`. Dependencies declared in `data-analysis/pyproject.toml` are installed into `claude-projects/.venv` when you run `uv sync` from the root.
