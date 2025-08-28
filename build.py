# ruff: noqa: S607
import shutil
import subprocess
import sys
from pathlib import Path

import PyInstaller.__main__
from rich.console import Console
from rich.prompt import Confirm, Prompt

console = Console()
try:
    console.rule("[bold yellow]preparing build[/]")
    if Path("./dist/").exists():
        delete = Confirm.ask("delete previous build?")
        if not delete:
            sys.exit(-1)
        console.print("deleting previous build...")
        shutil.rmtree(Path("./dist/"))
    console.print("writing commit_freeze.py")
    commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
    Path("./src/version/commit_freeze.py").write_text(f'commit = "{commit}"\n')
    console.print(f"wrote commit {commit}")
    answer = Prompt.ask("do you want to build to [bold yellow]one file[/] [italic grey50](1)[/], into [bold yellow]one directory[/] [italic grey50](2)[/] or [bold yellow]build an installer[/] [italic grey58](requires [link=https://sourceforge.net/projects/nsis/files/]NSIS[/link] to be installed)[/] [italic grey50](3)[/]?", choices=["1", "2", "3"], default="3")
    if answer == "1":
        console.rule("[bold yellow]building[/]")
        PyInstaller.__main__.run(["main-onefile.spec"])
    elif answer in ["2", "3"]:
        console.rule("[bold yellow]building app[/]")
        PyInstaller.__main__.run(["main-onedir.spec"])
        if answer == "3":
            console.rule("[bold yellow]building installer[/]")
            if not Path("C:\\Program Files (x86)\\NSIS\\makensis.exe").exists: 
                console.print("[bold][red]NSIS not installed![/bold] please install it from https://sourceforge.net/projects/nsis/files/.[/red]")
                console.print("[bold red]not building installer[/]")
                sys.exit(-1)
            from src.version.version import VERSION
            console.print(f"[italic]passing version [orange1]{VERSION}[/]")
            ret = subprocess.call(["C:\\Program Files (x86)\\NSIS\\makensis.exe", f"/DVERSION={VERSION}", "installer.nsh"])  # noqa: S603
            if ret != 0:
                console.print("[bold red]error! check output above.", ret)
            console.print("moving installer")
            Path("./excelmaplink-setup.exe").rename(Path("./dist/excelmaplink-setup.exe"))
    console.rule("[bold yellow]cleaning up[/]")
    console.print("deleting commit_freeze.py")
    Path("./src/version/commit_freeze.py").unlink()
    console.print("[green]done[/]")
except KeyboardInterrupt:
    console.print("[bold red] KeyboardInterrupt recieved.")
    Path("./src/version/commit_freeze.py").unlink()
    sys.exit(0)