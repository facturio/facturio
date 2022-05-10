# Facturio

**Facturio** est un logiciel de gestion de factures pour les systèmes d'exploitation GNU/Linux.
Il permet la création, customisation et sauvegarde des contrats qu'un professionnel effectue, ainsi que la génération automatique des factures associées.


# Installation

L'installation est très simple, il suffit de télécharger le script d'installation [install.sh](https://azaleth.xyz/install.sh), et de l'exécuter.
Tout sera automatiquement installé.

Pour une installation hors-ligne (ou derrière un proxy restrictif), on téléchargera les fichiers `install-networkless.sh` et `facturio-vTAG.tar.gz`, dans le même dossier, avant d'exécuter le premier.

# Construction du paquet à partir des sources

On utilisera une VM Ubuntu 22.04 pour générer le paquet (afin d'avoir un paquet reproducible.)

Après installation de la VM, et installation de notre éditeur favori  :

```sh
sudo apt install git python3-pip libosmgpsmap-1.0-1 gir1.2-osmgpsmap-1.0

mkdir -p facturio-1.0
cd facturio-1.0/
mkdir -p usr/bin/ usr/lib/x86_64-linux-gnu/girepository-1.0/ usr/lib/python3/dist-packages
cp -v /usr/bin/python3.10 usr/bin/
cp -v /usr/lib/python3/dist-packages/xdg usr/lib/python3/dist-packages
cp -v /usr/lib/x86_64-linux-gnu/libosmgpsmap-1.0.so.1.1.0 usr/lib/x86_64-linux-gnu/
cp -v /usr/lib/x86_64-linux-gnu/girepository-1.0/OsmGpsMap-1.0.typelib usr/lib/x86_64-linux-gnu/girepository-1.0/

cd ..
git clone https://github.com/facturio/facturio
cd facturio/
pip install --prefix ../facturio-1.0/usr .

cd ../facturio-1.0
chmod +x run.sh
tar czf ../facturio-1.0.tar.gz *
```
