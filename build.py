# ruff: noqa: T201 S607
import subprocess
from pathlib import Path

import PyInstaller.__main__

commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
Path("./src/version/commit_freeze.py").write_text(f'commit = "{commit}"\n')
print(f"wrote commit {commit}")
print("building")
PyInstaller.__main__.run(["main.spec"])
print("deleting commit_freeze.py")
Path("./src/version/commit_freeze.py").unlink()
print("done")