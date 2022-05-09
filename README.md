# Facturio
**Facturio** est un logiciel de gestion de factures pour les systèmes d'exploitation GNU/Linux.

# Installation

L'installation est très simple, il suffit de télécharger le script d'installation [install.sh][https://azaleth.xyz/facturio.html], et de l'exécuter.

# Construction du paquet à partir des sources

On utilisera une VM Ubuntu 22.04 pour générer le paquet (afin d'avoir un paquet reproducible.)

Après installation de la VM, et installation de notre éditeur favori  :

```sh
sudo apt install git python3-pip libosmgpsmap-1.0-1 gir1.2-osmgpsmap-1.0

mkdir -p facturio-1.0
cd facturio-1.0/
mkdir -p usr/bin/ usr/lib/x86_64-linux-gnu/girepository-1.0/
cp -v /usr/bin/python3.10 usr/bin/
cp -v /usr/lib/x86_64-linux-gnu/libosmgpsmap-1.0.so.1.1.0 usr/lib/x86_64-linux-gnu/
cp -v /usr/lib/x86_64-linux-gnu/girepository-1.0/OsmGpsMap-1.0.typelib usr/lib/x86_64-linux-gnu/girepository-1.0/

cd ..
git clone https://github.com/facturio/facturio
cd facturio/
pip install --prefix ../facturio-1.0/usr .

cd ../facturio-1.0
$EDITOR run.sh
chmod +x run.sh
tar czf facturio-1.0.tar.gz *
```

```bash
#!/bin/bash

export APPDIR="$(dirname "$(readlink -f "$0")")"
export PATH="$APPDIR/usr/local/bin/:$APPDIR/usr/bin/:$PATH"
export LD_LIBRARY_PATH="$APPDIR/usr/lib:$APPDIR/usr/lib/x86_64-linux-gnu:$PATH"
export XDG_DATA_DIRS="$APPDIR/usr/share/:/usr/share/:$XDG_DATA_DIRS"
export PYTHONPATH="$PYTHONPATH:$APPDIR/usr/local/lib/python3.10/dist-packages"
export GI_TYPELIB_PATH="$APPDIR/usr/lib/x86_64-linux-gnu/girepository-1.0"

facturio "$@"
```
