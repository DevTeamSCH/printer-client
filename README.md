# printer-client
## Követelmények
* Python 3
* Pip

## Telepítés
### Csomagok telepítése

A requirements mappában található fájlokban szereplő csomagokat kell feltelepíteni. A requirements.txt tartalmazza a fejlesztéshez tartozó követelményeket, a deployment.txt tartalmazza a python környezet nélkül futtathatóvá tételhez szükséges követelményeket. A telepítést ajánlott [pip-sync](https://github.com/jazzband/pip-tools)-el csinálni (`pip-sync requirements/requirements.txt`), de használható a síma pip is (`pip install -r requirements/requirements.txt`). Virtualenv használata ajánlott.

### UI fájlok
A design mappában található ui fájlok Qt Designer-el szerkeszthetőek. A .ui fájlokból generálni kell python kódot, ehhez a pyuic használható. Windows-on a főmappában található `generateui.bat` és `generateui.ps1` szkriptek ezt minden ui fájlra megcsinálják. Más platformokon a következő parancsot kell lefutatni minden design mappában lévő .ui fájlra:

`pyuic {fájlnév}.ui > {fájlnév}_ui.py`

### Futtatás
`python main.py`

## Futthatható fájlok előállítása
### PyInstaller
PyInstaller-el minden platformon előállítható python környezet nélkül működő alkalmazás. Csak a használt python verzióhoz és operációs rendszerhez állítható elő. A következő parancsot kell futtatni:

`pyinstaller main.py --windowed`

Ez a dist mappába helyezi az operációs rendszernek megfelelő programot.

### Inno Setup
Windows-os telepítő program az [Inno Setup](http://www.jrsoftware.org/isinfo.php)-al készíthető. Telepítés után a `iscc printer_client.iss` parancsal az Output mappába kerül egy telepítő exe. A verzió megadható manuálisan is a /DVersion=<verzió> kapcsoló használatával.