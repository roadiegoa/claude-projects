# Post-Reboot Checklist

## Step 1 — Set PowerShell Execution Policy

Run in PowerShell (admin rights required):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Verify it took:

```powershell
Get-ExecutionPolicy -List
# CurrentUser should show RemoteSigned
```

## Step 2 — Register the claude-projects Kernel

```powershell
cd C:\Users\droa\Documents\Workspace\claude-projects
uv-kernel-smart
```

## Step 3 — Launch JupyterLab and Switch Kernel

```powershell
jlab
```

1. Open your notebook in `data-analysis/`
2. Click the kernel name (top-right) and select **"Python (claude-projects)"**
3. Verify pandas is available:

```python
import pandas as pd
print(pd.__version__)
```
