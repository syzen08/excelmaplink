# excelmaplink
<p align="center">
  <a href="http://forthebadge.com/"><img src="https://forthebadge.com/images/badges/powered-by-qt.svg" alt="forthebadge"/></a>
  <a href="http://forthebadge.com/"><img src="https://forthebadge.com/images/badges/made-in-python.svg" alt="forthebadge"/></a>
  <a href="http://forthebadge.com/"><img src="https://forthebadge.com/images/badges/platform-windows.svg" alt="forthebadge"/></a>
  <br>
  <a href="http://forthebadge.com/"><img src="https://forthebadge.com/images/badges/contains-tasty-spaghetti-code.svg" alt="forthebadge"/></a>
  <a href="http://forthebadge.com/"><img src="https://forthebadge.com/images/badges/powered-by-black-magic.svg" alt="forthebadge"/></a>
  <a href="http://forthebadge.com/"><img src="https://forthebadge.com/images/badges/approved-by-my-mom.svg" alt="forthebadge"/></a>
</p>

a interactive map allowing the user to toggle regions on the map which also toggles values in an excel spreadsheet. 

> [!IMPORTANT]
> this is only tested on windows. if you're feeling lucky, you can try it on macOS as well.

## Running
**Excel has to be installed!**

get the latest .exe from the [releases](https://github.com/syzen08/excelmaplink/releases)

## Building
> [!NOTE]
> all the following commands are for powershell (yes i'm a masochist)

first, clone the repository (this requires [git](https://git-scm.com/downloads) to be installed) and cd into it
```
git clone https://github.com/syzen08/excelmaplink.git
cd excelmaplink
```
create a venv and activate it:
```
python -m venv .\.venv
.\.venv\Scripts\Activate.ps1
```
install the dependencies using pip
```
pip install -r requirements.txt
```
you can now run the app using
```
python main.py
```
if you want to (nice for development).

to build the executable, run
```
pyinstaller .\main.spec
```
the finished executable will be in the `dist` folder.

## Translation
from inside the venv run 
```
.\translate.ps1
```
this will update the translation files and open Linguist.

once you're done, save and close Linguist and it will generate the .qm binaries.

make sure to run
```
pyside6-rcc .\resources.qrc -o .\resources_rc.py
```
to update the resources used by qt.
