import os
import subprocess
from pathlib import Path

import PyInstaller.__main__

commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
Path("./src/version/commit_freeze.py").write_text(f'commit = "{commit}"\n')
print(f"wrote commit {commit}")
print("building")
PyInstaller.__main__.run(["main.spec"])
print("deleting commit_freeze.py")
os.remove(Path("./src/version/commit_freeze.py"))
print("done")